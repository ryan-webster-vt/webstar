import pandas as pd
import time
import random
import datetime
import os

def scrape_data(team: str, year: int):
    """
    Scrape and format NCAA men's basketball game logs for a given team and season.

    Pulls data from Sports Reference, removes extraneous rows, computes possessions
    and points per possession (PPP), and returns a game-level DataFrame.

    Parameters
    ----------
    team : str
        Sports Reference team identifier.
    year : int
        Season year (e.g., 2024 for the 2023-24 season).

    Returns
    -------
    pandas.DataFrame
        Game-level data with opponent, location flags, points, possessions,
        PPP metrics, and a unique game_id.
    """

    # Read data
    url = f"https://www.sports-reference.com/cbb/schools/{team}/men/{year}-gamelogs.html"
    tables = pd.read_html(url)
    df = tables[0]

    # Remove Extranious Rows
    df = df[df[('Unnamed: 0_level_0', 'Rk')] != 'Rk']
    df = df[~df[('Unnamed: 1_level_0', 'Gtm')].isna()]

    # Extract neccessary data
    formatted_df = pd.DataFrame({
        'team' : [team] * len(df),
        'year' : [year] * len(df)
    })

    # Format data
    formatted_df['opponent'] = df[('Unnamed: 4_level_0', 'Opp')]

    loc = df[('Unnamed: 3_level_0', 'Unnamed: 3_level_1')]
    formatted_df['home'] = loc.isna()
    formatted_df['neutral'] = loc == 'N'
    formatted_df['away'] = loc == '@'

    formatted_df['points_team'] = df[('Score', 'Tm')].astype(int)
    formatted_df['points_opponent'] = df[('Score', 'Opp')].astype(int)

    formatted_df['possession_team'] = (
        df[('Team', 'FGA')].astype(int) - 
        df[('Team', 'ORB')].astype(int) + 
        df[('Team', 'TOV')].astype(int) + 
        (0.44 * df[('Team', 'FTA')].astype(int))
    )

    formatted_df['possession_opponent'] = (
        df[('Opponent', 'FGA')].astype(int) - 
        df[('Opponent', 'ORB')].astype(int) + 
        df[('Opponent', 'TOV')].astype(int) + 
        (0.44 * df[('Opponent', 'FTA')].astype(int))
    )

    formatted_df['ppp_off_team'] = formatted_df['points_team'] / formatted_df['possession_team']
    formatted_df['ppp_def_team'] = formatted_df['points_opponent'] / formatted_df['possession_opponent']
    formatted_df['ppp_off_opp'] = formatted_df['ppp_def_team'] 
    formatted_df['ppp_def_opp'] = formatted_df['ppp_off_team']

    formatted_df['game_id'] = (df[('Unnamed: 2_level_0', 'Date')] + team + formatted_df['opponent']).str.lower().str.replace(" ", "").str.replace("-", "")

    return formatted_df

def main():
    print(os.getcwd())
    team_list = pd.read_json('data/master_team_list.json', orient='values')
    team_list = team_list[0]

    main_df = pd.DataFrame()
    for i, team in enumerate(team_list, start=1):
        print(team)

        try:
            df = scrape_data(team, 2026)
        except Exception as e:
            print(f"ERROR {team} : {e}")
            time.sleep(random.uniform(3, 5))
            continue
        
        main_df = pd.concat([main_df, df])
        print(f"{i}/{len(team_list)}")
        time.sleep(random.uniform(3, 5))

    # Remove non-division one matchups
    main_df = main_df[main_df['team'].isin(team_list)]

    today = datetime.datetime.now()
    main_df.to_csv("data/master_df.csv", index=False)

if __name__ == "__main__":
    print(datetime.datetime.now())
    main()
