import pandas as pd
import requests
from bs4 import BeautifulSoup
from clean_names import clean_names

def retrieve_team_list():
    # Read Data
    url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
    tables = pd.read_html(url)
    df = tables[0]

    # Remove header rows, return series of schools
    schools = df[(df[('Unnamed: 0_level_0', 'Rk')] != 'Rk') & (~df[('Unnamed: 0_level_0', 'Rk')].isna())][('Unnamed: 1_level_0', 'School')]
    schools = clean_names(schools)
    return schools

def main():
    pd.Series(retrieve_team_list().tolist()).to_json('data/master_team_list.json', orient = 'records')

if __name__ == "__main__":
    main()