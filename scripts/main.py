import logging
from zoneinfo import ZoneInfo
from datetime import datetime, time

from scrape_data_v2 import main as main_scrape_data
from scrape_todays_games import main as main_scrape_todays_games
from execute_mcmc import main as main_execute_mcmc

logging.basicConfig(
    filename='../logs/pipeline.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def is_allowed_time():
    est = ZoneInfo("America/New_York")
    now = datetime.now(est).time()

    start = time(7, 55)
    end = time(8, 5)

    return start <= now <= end

def main():
    if not is_allowed_time():
        logging.info("Execution blocked: not within 7:55-8:05 AM EST window.")
        return

    logging.info(f"Starting pipeline")
    try:
        logging.info(f"Scraping today's games...")
        main_scrape_todays_games()

        logging.info(f"Scraping boxscore data...")
        main_scrape_data()

        logging.info(f"Running MCMC model...")
        main_execute_mcmc()

        logging.info(f"Pipeline finished")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
