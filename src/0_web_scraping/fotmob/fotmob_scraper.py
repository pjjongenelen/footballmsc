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
    "Given a string that is a concatenation of a jersey number and the name, return the two substring seperate"

    num = [letter for letter in string if letter.isdigit()]
    num = "".join(map(str, num))
    nam = [letter for letter in string if not letter.isdigit()]
    nam = "".join(map(str, nam))

    return num, nam
    
def get_field_df(soup):
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
    bench_ratings = []
    bench_players = []
    bench_numbers = []
    for subsoup in soup.find_all(class_=re.compile("LeftBenchItem ")):  # the space is very important in the regex
        if 'PlayerRating' in str(subsoup):
            # extract name and number
            num, name = convert_num_nam((subsoup.find_all('span')[-2].get_text()))
            bench_players.append(name)
            bench_numbers.append(num)

            # get rating
            rating_element = subsoup.find(class_=re.compile("PlayerRatingStyled"))
            bench_ratings.append(rating_element.find('span').get_text())

    return pd.DataFrame({"number": bench_numbers, "name": bench_players, "rating": bench_ratings})

if __name__ == "__main__":
    # first we need to get the list of urls of all the match summary pages
    urls = []
    for playing_round in tqdm(range(1, 3), desc="scraping urls"):
        page = requests.get(f"https://www.fotmob.com/leagues/57/matches/eredivisie?page={playing_round}")
        soup = BeautifulSoup(page.content, "html.parser")
        
        for a in soup.find_all("a"):
            url_end = a['href']
            if 'matchfacts' in url_end:
                urls.append(f"https://www.fotmob.com{url_end}")

    # now let's scrape the player grades from each of these urls
    ratings = pd.DataFrame()

    for url in tqdm(urls, desc = "scraping grades"):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        new_ratings = pd.concat([get_field_df(soup), get_bench_df(soup)])
        home, away = url.split("/")[-1].split("-vs-")
        new_ratings['home'], new_ratings['away'] = home, away

        ratings = pd.concat([ratings, new_ratings]).reset_index(drop=True)

    print(ratings)
    # ratings.to_pickle(f"{ROOT}/data/raw/fotmob_ratings.pkl")

    