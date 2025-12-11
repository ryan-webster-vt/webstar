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
    df = tables[0]

def main():
    get_schedule(datetime.datetime.month, datetime.datetime.day, datetime.datetime.year)

if __name__ == "__main__":
    main()


