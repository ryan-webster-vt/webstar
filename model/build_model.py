import pandas as pd
import pymc as pm
import arviz as az
import numpy as np

# Example game-level data
data = pd.DataFrame({
    'Team': ['A','B','A','C','B'],
    'Opponent': ['X','Y','Y','X','Z'],
    'Points': [100, 90, 110, 95, 105],
    'Possessions': [95, 90, 100, 92, 98]
})

# Compute PPP
data['PPP'] = data['Points'] / data['Possessions']

# Encode categorical variables as indices
teams = data['Team'].unique()
team_idx = data['Team'].apply(lambda x: np.where(teams == x)[0][0])
opponents = data['Opponent'].unique()
opp_idx = data['Opponent'].apply(lambda x: np.where(opponents == x)[0][0])

with pm.Model() as model:
    # League average PPP (fixed effect)
    mu = pm.Normal('mu', mu=1, sigma=0.5)
    
    # Random effects for teams (offense)
    sigma_team = pm.HalfNormal('sigma_team', sigma=0.5)
    team_offense = pm.Normal('team_offense', mu=0, sigma=sigma_team, shape=len(teams))
    
    # Random effects for opponents (defense)
    sigma_opp = pm.HalfNormal('sigma_opp', sigma=0.5)
    opp_defense = pm.Normal('opp_defense', mu=0, sigma=sigma_opp, shape=len(opponents))
    
    # Expected PPP
    ppp_hat = mu + team_offense[team_idx] - opp_defense[opp_idx]
    
    # Likelihood
    sigma = pm.HalfNormal('sigma', sigma=0.1)
    y = pm.Normal('y', mu=ppp_hat, sigma=sigma, observed=data['PPP'])
    
    # Sample posterior
    trace = pm.sample(2000, tune=1000, target_accept=0.9)

# Examine results
az.summary(trace, var_names=['mu', 'team_offense', 'opp_defense'])
