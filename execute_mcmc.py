import pandas as pd
import pymc as pm
import arviz as az
import numpy as np
from clean_names import clean_names, clean_opponent_names, display_names
from datetime import datetime
from zoneinfo import ZoneInfo

# Read Data
df = pd.read_csv('data/master_df.csv')

team_list = pd.read_json('data/master_team_list.json', orient='values')
team_list = team_list[0]

# Create Win/Loss table
df['result'] = np.where(df['points_team'] > df['points_opponent'], 'W', 'L')
records = (
    df.groupby('team')['result']
      .value_counts()
      .unstack(fill_value=0)
)

# Little more cleaning
df = df[~df['opponent'].isna()]
df['opponent'] = clean_opponent_names(df['opponent'])
df = df[df['opponent'].isin(team_list)]

# Encode categorical variables as indices
teams = df['team'].unique()
team_idx = df['team'].apply(lambda x: np.where(teams == x)[0][0])
opponents = df['opponent'].unique()
opp_idx = df['opponent'].apply(lambda x: np.where(opponents == x)[0][0])

conditions = [
    df['home'] == True,
    df['away'] == True,
    df['neutral'] == True
]

choices = [1, -1, 0]

df['location'] = np.select(conditions, choices, default=0)

with pm.Model() as model:
    
    # League average PPP
    mu = pm.Normal('mu', mu=1, sigma=0.5)
    
    # Team random effects (offense)
    sigma_team = pm.HalfNormal('sigma_team', sigma=1.0)
    team_off_raw = pm.Normal('team_off_raw', mu=0, sigma=1, shape=len(teams))
    team_off = pm.Deterministic('team_off', sigma_team * (team_off_raw))
    
    # Opponent random effects (defense)
    sigma_opp = pm.HalfNormal('sigma_opp', sigma=1.0)
    opp_def_raw = pm.Normal('opp_def_raw', mu=0, sigma=1, shape=len(opponents))
    opp_def = pm.Deterministic('opp_def', sigma_opp * (opp_def_raw))
    
    # Home-court effect
    beta_home = pm.Normal('beta_home', mu=0, sigma=0.02)
    
    # Expected PPP for each game
    ppp_hat = (
        mu
        + team_off[team_idx]             # offense of team
        - opp_def[opp_idx]               # defense of opponent
        + beta_home * df['location']         # home-court
    )
    
    # Likelihood
    sigma = pm.HalfNormal('sigma', sigma=0.1)
    y = pm.Normal('y', mu=ppp_hat, sigma=sigma, observed=df['ppp_off_team'])
    
    # Sample posterior
    trace = pm.sample(1000, tune=500, target_accept=0.9, progressbar=True)

# Examine results
az.summary(trace, var_names=["mu", "team_off", "opp_def", "beta_home"])

teams = df['team'].unique()
team_idx_map = {team: i for i, team in enumerate(teams)}

opponents = df['opponent'].unique()
opp_idx_map = {opp: i for i, opp in enumerate(opponents)}

adj_off_eff = {}
for team, i in team_idx_map.items():
    off_samples = trace.posterior['team_off'].sel(team_off_dim_0=i)
    adj_off_eff[team] = (trace.posterior['mu'].mean().item() + off_samples.mean().item())

adj_def_eff = {}
for opp, i in opp_idx_map.items():
    def_samples = trace.posterior['opp_def'].sel(opp_def_dim_0=i)
    adj_def_eff[opp] = (trace.posterior['mu'].mean().item() - def_samples.mean().item())

off_df = pd.DataFrame({
    'Team': list(adj_off_eff.keys()),
    'AdjOffEff': list(adj_off_eff.values())
})

def_df = pd.DataFrame({
    'Team': list(adj_def_eff.keys()),
    'AdjDefEff': list(adj_def_eff.values())
})

rankings = off_df.merge(def_df, on="Team", how="left")
rankings = rankings.merge(records, left_on='Team', right_on='team')

# Add Rank
rankings['Total'] = rankings['AdjOffEff'] - rankings['AdjDefEff']
rankings = rankings.sort_values('Total', ascending=False)
rankings['Rank'] = range(1, len(rankings) + 1)

# Add Date
eastern = ZoneInfo("America/New_York")
rankings['Date'] = datetime.now(tz=eastern).date()

print(rankings)

# Making the data table pretty
rankings['Team'] = rankings['Team'].str.title()
rankings['Team'] = rankings['Team'].str.replace('-', ' ')
rankings['Team'] = display_names(rankings['Team'])

rankings = rankings[['Rank', 'Team', 'Total', 'W', 'L', 'AdjOffEff', 'AdjDefEff', 'Date']]
rankings[['Total', 'AdjOffEff', 'AdjDefEff']] = (rankings[['Total', 'AdjOffEff', 'AdjDefEff']] * 100).round(2)

# Concat to current rankings
current_rankings = pd.read_csv('data/current_rankings.csv')
final_rankings = pd.concat([current_rankings, rankings], ignore_index = True)
final_rankings.to_csv('data/current_rankings.csv', index = False)
