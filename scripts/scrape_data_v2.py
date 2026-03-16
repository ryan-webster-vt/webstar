import cbbpy.mens_scraper as s
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import boto3
import io
from zoneinfo import ZoneInfo

def retrieve_game(game_id: int):
    """
    Returns boxscore_df and info_df for a single game.
    """
    info_df, boxscore_df, _= s.get_game(game_id=game_id, pbp=False, info=True)
    return boxscore_df, info_df

def compute_possessions(fga, fta, oreb, to):
    """Estimate possessions for a team."""
    return fga - oreb + to + (0.44 * fta)

def scrape_data(days_ago=1):
    """
    Scrapes all games from a given day.
    Returns two lists: boxscores and info dataframes.
    """
    date = datetime.now(ZoneInfo("America/New_York")) - timedelta(days=days_ago)
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
    boxscores = pd.concat(boxscores, ignore_index=True)
    info_list = pd.concat(info_list, ignore_index=True)

    return boxscores, info_list

def build_matchup_table(boxscores, info_list):
    """
    Combine boxscore and info_df to create matchup table with home/away/neutral.
    """
    # 
    boxscores = boxscores[boxscores['player'] == 'TEAM']
    cols = ['game_id', 'team', 'pts', 'fga', 'fta', 'oreb', 'to']
    boxscores = boxscores[cols]

    # Each game has two rows — split into "team" and "opponent" by pairing them
    df1 = boxscores.iloc[::2].reset_index(drop=True)   # first team in each game
    df2 = boxscores.iloc[1::2].reset_index(drop=True)  # second team in each game

    # Join side by side
    merged = pd.concat([
        df1.rename(columns=lambda c: c if c == 'game_id' else f'team_{c}'),
        df2.rename(columns=lambda c: f'opp_{c}' if c != 'game_id' else c).drop(columns='game_id')
    ], axis=1)

    # Create inverse rows (swap team/opp)
    inverse = merged.rename(columns=lambda c: c.replace('team_', '__tmp__').replace('opp_', 'team_').replace('__tmp__', 'opp_'))

    # Stack original + inverse
    result = pd.concat([merged, inverse], ignore_index=True).sort_values('game_id').reset_index(drop=True)

    result = result.merge(info_list[['game_id', 'home_team', 'is_neutral', 'game_day']], on = 'game_id')
    result = result.rename(columns={'team_team': 'team'})
    
    result['neutral'] = result['is_neutral'] == 1
    result['home'] = (~result['neutral']) & (result['home_team'] == result['team'])
    result['away'] = (~result['neutral']) & (result['home_team'] != result['team'])

    result['possession_team'] = compute_possessions(result['team_fga'], result['team_fta'], result['team_oreb'], result['team_to'])
    result['possession_opp'] = compute_possessions(result['opp_fga'], result['opp_fta'], result['opp_oreb'], result['opp_to'])

    result['ppp_off_team'] = result['team_pts']/ result['possession_team']
    result['ppp_def_team'] = result['opp_pts'] / result['possession_opp']

    result['ppp_off_opp'] = result['opp_pts'] / result['possession_opp'] 
    result['ppp_def_opp'] = result['team_pts'] / result['possession_team']

    return result

def main():
    # Open data to concat to from S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='webstar-bucket', Key='master_df.csv')
    prev_master_df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Scrape/clean data
    box_scores, info_list = scrape_data()

    # If no games, abrupt script
    if len(box_scores) == 0:
        return

    matchup_df = build_matchup_table(box_scores, info_list)

    # Concat data to existing master file
    master_df = pd.concat([prev_master_df, matchup_df], ignore_index= True)

    # Removes duplicate data if manually ran on the same day
    master_df = master_df.drop_duplicates(
        subset = ['game_id', 'team', 'opp_team'],
        keep = 'first'
    ).reset_index(drop=True)

    # Save data onto S3
    csv_buffer = io.StringIO()
    master_df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket = 'webstar-bucket',
        Key = 'master_df.csv',
        Body = csv_buffer.getvalue()
    )

if __name__ == "__main__":
    main()
    
