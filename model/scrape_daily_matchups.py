import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import time
import random

def get_schedule(month, day, year):
    # Read data
    url = f"https://www.sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}"
    tables = pd.read_html(url)
    df = tables[30]
    print(df)


def main():
    today = datetime.datetime.now()
    get_schedule(today.month, today.day, today.year)

if __name__ == "__main__":
    main()


