import cbbpy.mens_scraper as s
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import boto3
import io

def retrieve_game(game_id: int):
    _, boxscore_df, info_df = s.get_game(game_id=game_id, pbp=False, info=True)
    return boxscore_df, info_df

def compute_possessions(fga, fta, oreb, to):
    return fga - oreb + to + (0.44 * fta)

def scrape_data(days_ago=1):
    """
    Scrapes all games from a given day.
    Returns two lists: boxscores and info dataframes.
    """
    date = datetime.today() - timedelta(days=days_ago)
    game_ids = s.get_game_ids(date)

    if not game_ids:
        print(f"No games found on {date.strftime('%Y-%m-%d')}")
        return [], []

    print(f"Found {len(game_ids)} game(s) on {date.strftime('%Y-%m-%d')}")

    boxscores = []
    info_list = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_gid = {executor.submit(retrieve_game, gid): gid for gid in game_ids}
        for i, future in enumerate(as_completed(future_to_gid), start=1):
            gid = future_to_gid[future]
            try:
                boxscore_df, info_df = future.result()
                boxscores.append(boxscore_df)
                info_list.append(info_df)
                print(f"Retrieved {gid} ({i}/{len(game_ids)})")
            except Exception as e:
                print(f"Failed to retrieve {gid}: {e}")

    print("All games scraped!")
    return boxscores, info_list

def build_matchup_table(boxscores, info_list):
    """
    Combine boxscore and info_df to create matchup table with home/away/neutral.
    """
    # 
    boxscores = boxscores[boxscores['player'] == 'TEAM']
    cols = ['game_id', 'team', 'pts', 'fga', 'fta', 'oreb', 'to']
    boxscores = boxscores[cols]

    df_team = boxscores.copy()
    df_opp  = boxscores.add_prefix('opp_').rename(columns={'opp_game_id': 'game_id', 'opp_team': 'opponent'})
    result = df_team.merge(df_opp, on='game_id')
    result = result[result['team'] < result['opponent']].reset_index(drop=True)

    result = result.merge(info_list[['game_id', 'home_team', 'is_neutral', 'game_day']], on = 'game_id')
    result['neutral'] = result['is_neutral'] == 1
    result['home'] = (~result['neutral']) & (result['home_team'] == result['team'])
    result['away'] = (~result['neutral']) & (result['home_team'] != result['team'])

    result['possession_team'] = compute_possessions(result['fga'], result['fta'], result['oreb'], result['to'])
    result['possession_opp'] = compute_possessions(result['opp_fga'], result['opp_fta'], result['opp_oreb'], result['opp_to'])

    result['ppp_off_team'] = result['pts'] / result['possession_team']
    result['ppp_def_team'] = result['opp_pts'] / result['possession_opp']

    result['ppp_off_opp'] = result['opp_pts'] / result['possession_opp']
    result['ppp_def_opp'] = result['pts'] / result['possession_team']

    result = result[['team', 'opponent', 'home', 'neutral', 'away', 'pts', 'opp_pts', 'possession_team', 
                    'possession_opp', 'ppp_off_team', 'ppp_def_team', 'ppp_off_opp', 'ppp_def_opp', 'game_id', 'game_day']]

    return result

def main():
    # Open data to concat to from S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='webstar-bucket', Key='data/master_df.csv')
    prev_master_df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Scrape/clean data
    box_scores, info_list = scrape_data()
    matchup_df = build_matchup_table(box_scores, info_list)

    # Concat data to existing master file
    master_df = pd.concat(prev_master_df, matchup_df, ignore_index= True)

    # Save data
    master_df.to_csv('data/master_df.csv', index = False)


if __name__ == "__main__":
    main()
    
