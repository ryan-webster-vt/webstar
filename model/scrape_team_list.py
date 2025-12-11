import pandas as pd
import requests
from bs4 import BeautifulSoup

def retrieve_team_list():
    # Read Data
    url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
    tables = pd.read_html(url)
    df = tables[0]

    # Remove header rows, return series of schools
    df = df[(df[('Unnamed: 0_level_0', 'Rk')] != 'Rk') & (~df[('Unnamed: 0_level_0', 'Rk')].isna())]
    return(df[('Unnamed: 1_level_0', 'School')].str.lower().str.replace(" ", "-").str.replace("&", "").str.replace("(", "")).str.replace(")", "")

def main():
    retrieve_team_list().to_json("data/team_list.json")

if __name__ == "__main__":
    main()