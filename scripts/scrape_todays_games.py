import pandas as pd
import cbbpy.mens_scraper as s
import boto3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from scipy.stats import norm
import io
import numpy as np
import os


import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.clean_names import normalize_team_name

s3 = boto3.client('s3')

def home_team_spread(home, away, neutral):
    spread = (home - away) * 0.679
    spread += (~neutral) * 2.9
    return spread

def home_team_wp(home_spread):
    home_wp = 1 - norm.cdf(0, loc=home_spread, scale=10)
    away_wp = 1 - home_wp
    return home_wp

def scrape_games():
    today = datetime.now(ZoneInfo("America/New_York"))
    todays_games_ids = s.get_game_ids(date=today)

    games = []

    for i, game_id in enumerate(todays_games_ids, start=1):
        try:
            game, _, _ = s.get_game(game_id, box = False, pbp = False)
            games.append(game)
            print(f'Successfully recieved {game_id}! - {i} / {len(todays_games_ids)}')
        except Exception as e:
            print(f"Failed to retrieve {game_id}: {e}")

    schedule = pd.concat(games, ignore_index=True)

    return schedule

def calculate_spreads_wp(schedule):
    # Read rankings data from S3
    obj = s3.get_object(Bucket='webstar-bucket', Key='current_rankings.csv')
    current_rankings = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Filter by today's data
    current_rankings['Date'] = pd.to_datetime(current_rankings['Date']).dt.date
    today = datetime.now(ZoneInfo("America/New_York")).date()
    current_rankings = current_rankings[current_rankings['Date'].dt.date == today]

    # Select necessary cols, normalize teams name
    cols = ['game_id', 'home_team', 'away_team', 'is_neutral', 'game_time', 'tv_network']
    schedule = schedule[cols]
    schedule['home_team'] = schedule['home_team'].apply(normalize_team_name)
    schedule['away_team'] = schedule['away_team'].apply(normalize_team_name)

    # Map teams net values onto schedule
    team_rating_map = current_rankings.set_index('Team')['Total']
    print(team_rating_map)
    schedule['home_team_rating'] = schedule['home_team'].map(team_rating_map)
    schedule['away_team_rating'] = schedule['away_team'].map(team_rating_map)

    # Calculate home win spreads/wp
    schedule['home_team_spread'] = home_team_spread(schedule['home_team_rating'], schedule['away_team_rating'], schedule['is_neutral'])
    schedule['home_team_wp'] = home_team_wp(schedule['home_team_spread'])
    schedule['away_team_wp'] = 1 - schedule['home_team_wp']
    schedule['home_team_spread'] = schedule['home_team_spread'] * -1

    # Clean up
    schedule[['home_team_wp', 'away_team_wp']] = (schedule[['home_team_wp', 'away_team_wp']] * 100).round(2)
    schedule['home_team_spread'] = schedule['home_team_spread'].round(1)

    # Add team label for spread
    schedule['home_team_spread_display'] = (
    schedule['home_team'] + ' ' +
    np.where(
        schedule['home_team_spread'] > 0,
        '+' + schedule['home_team_spread'].astype(str),
        schedule['home_team_spread'].astype(str)
    )
)

    schedule['date'] = datetime.now(ZoneInfo("America/New_York"))

    return schedule

def main():
    schedule = scrape_games()
    final_schedule = calculate_spreads_wp(schedule)

    # Save data onto S3
    csv_buffer = io.StringIO()
    final_schedule.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket = 'webstar-bucket',
        Key = 'todays_games.csv',
        Body = csv_buffer.getvalue()
    )

if __name__ == "__main__":
    main()