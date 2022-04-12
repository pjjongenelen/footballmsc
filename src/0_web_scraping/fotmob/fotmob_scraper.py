"""
Scrapes player names, jersey numers, and grades for the Eredivisie seasons 2021-2022 from fotmob.com
Contrary to the other scrapers, I just use BeautifulSoup here, instead of Scrapy
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from tqdm import tqdm


ROOT = "C:/Users/timjo/python_projects/footballmsc"


def convert_num_nam(string):
    "Small helper function, input '30Thomassen' is returned as (30, Thomassen)"

    # extract jersey number
    num = [letter for letter in string if letter.isdigit()]
    num = "".join(map(str, num))
    # extract player name
    nam = [letter for letter in string if not letter.isdigit()]
    nam = "".join(map(str, nam))

    return num, nam
    
def get_field_df(soup):
    """
    """

    field_ratings = []
    field_players = []
    field_numbers = []
    for field_player in soup.find_all(class_=re.compile("LineupPlayerContainer")):
        rating_element = field_player.find_all(class_=re.compile("PlayerRatingStyled"))
        if len(rating_element) == 0:
            field_ratings.append("nan")
        else:
            field_ratings.append(rating_element[0].find_all("span")[0].get_text())
        
        player_text = field_player.find(class_=re.compile("LineupPlayerText"))
        num, name = convert_num_nam(player_text.get_text())
        field_players.append(name)
        field_numbers.append(num)

    return pd.DataFrame({"number": field_numbers, "name": field_players, "rating": field_ratings})
    
def get_bench_df(soup):
    """
    """

    bench_ratings = []
    bench_players = []
    bench_numbers = []
    for subsoup in soup.find_all(class_=re.compile("LeftBenchItem ")):  # the space is very important in the regex
        if 'PlayerRating' in str(subsoup):
            # extract name and number
            num, name = convert_num_nam((subsoup.find_all('span')[-2].get_text()))
            bench_players.append(name)
            bench_numbers.append(num)

            # extract rating
            rating_element = subsoup.find(class_=re.compile("PlayerRatingStyled"))
            bench_ratings.append(rating_element.find('span').get_text())

    return pd.DataFrame({"number": bench_numbers, "name": bench_players, "rating": bench_ratings})


def generate_match_urls(last_playing_round: int) -> list:
    """
    Returns all Eredivisie match urls from fotmob.com for the 21-22 season up until a given playing round
    """

    urls = []
    for playing_round in tqdm(range(1, last_playing_round), desc="scraping urls"):
        page = requests.get(f"https://www.fotmob.com/leagues/57/matches/eredivisie?page={playing_round}")
        soup = BeautifulSoup(page.content, "html.parser")
        
        for a in soup.find_all("a"):
            url_end = a['href']
            if 'matchfacts' in url_end:
                urls.append(f"https://www.fotmob.com{url_end}")
    
    return urls

def scrape_player_grades(urls):
    # now let's scrape the player grades from each of these urls
    ratings = pd.DataFrame()

    for url in tqdm(urls[:3], desc = "scraping grades"):
        # get page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # get ratings from this match page
        new_ratings = pd.concat([get_field_df(soup), get_bench_df(soup)])
        home, away = url.split("/")[-1].split("-vs-")

        # get home and away team, and fotmob match id
        new_ratings['home'], new_ratings['away'] = home, away
        new_ratings['fotmob_match_id'] = url.split("/")[-3]

        # add current ratings to df
        ratings = pd.concat([ratings, new_ratings]).reset_index(drop=True)
    
    return ratings


if __name__ == "__main__":
    # get match urls
    url_list = generate_match_urls(last_playing_round = 28)
    # scrape grades
    fotmob_grades_df = scrape_player_grades(urls = url_list)    

    # output
    print(fotmob_grades_df)
    # ratings.to_pickle(f"{ROOT}/data/raw/fotmob_ratings.pkl")

    