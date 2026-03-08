import boto3
import pandas as pd
import io
import cbbpy.mens_scraper as s


s3 = boto3.client('s3')

def main():
    # Retrieve yesterday's games
    obj = s3.get_object(Bucket='webstar-bucket', Key='todays_games.csv')
    yesterdays_games = pd.read_csv(io.BytesIO(obj['Body'].read()))

    if len(yesterdays_games) == 0:
        print(f"No games to archive. Aborting...")
        return

    # Retrieve results of yesterday's games
    results = []

    for i, game_id in enumerate(yesterdays_games['game_id'], start=1):
        try:
            game, _, _ = s.get_game(game_id, box = False, pbp = False)
            results.append(game)
            print(f'Successfully recieved {game_id}! - {i} / {len(yesterdays_games['game_id'])}')
        except Exception as e:
            print(f"Failed to retrieve {game_id}: {e}")

    results = pd.concat(results, ignore_index=True)[['game_id', 'home_score', 'away_score', 'game_day']]

    # Merge results onto yesterday's games
    results['game_id'] = results['game_id'].astype('Int64')
    yesterdays_games = pd.merge(yesterdays_games, results, on='game_id')

    yesterdays_games['home_dff'] = yesterdays_games['home_score'] - yesterdays_games['away_score']
    yesterdays_games['home_error'] = yesterdays_games['home_dff'] - (yesterdays_games['home_team_spread'] * -1)
    yesterdays_games['home_error_abs'] = abs(yesterdays_games['home_error'])

    # Concat onto existing archive
    obj = s3.get_object(Bucket='webstar-bucket', Key='archived_results.csv')
    archived_results = pd.read_csv(io.BytesIO(obj['Body'].read()))
    archived_results = pd.concat([archived_results, yesterdays_games], ignore_index=True)
    archived_results = archived_results.drop_duplicates(subset=["game_id", 'game_day'])

    # Save onto S3
    csv_buffer = io.StringIO()
    archived_results.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket = 'webstar-bucket',
        Key = 'archived_results.csv',
        Body = csv_buffer.getvalue()
    )

if __name__ == "__main__":
    main()