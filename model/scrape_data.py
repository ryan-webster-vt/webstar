import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import datetime

def scrape_data(team, year):
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


    today = datetime.datetime.now()
    main_df.to_csv(f"master_df.csv")

if __name__ == "__main__":
    main()


