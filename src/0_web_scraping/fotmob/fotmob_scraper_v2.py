"""
DOCSTRING
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from tqdm import tqdm

ROOT = "C:/Users/timjo/OneDrive - TU Eindhoven/Silva_Ducis/Scriptie/footballmsc"


def generate_match_urls(last_playing_round: int) -> list:
    """
    Returns all Eredivisie match urls from fotmob.com for the 21-22 season up until a given playing round
    """

    urls = []
    for playing_round in tqdm(range(1, last_playing_round + 1), desc="scraping urls"):
        # get the webpage for this playing round
        page = requests.get(
            f"https://www.fotmob.com/leagues/57/matches/eredivisie?page={playing_round}")
        soup = BeautifulSoup(page.content, "html.parser")

        # goes through all urls on the page, finding those that contain 'matchfacts', these are the ones we're looking for
        for a in soup.find_all("a"):
            url_end = a['href']
            if 'matchfacts' in url_end:
                urls.append(f"https://www.fotmob.com{url_end}")

    return urls


def standardize_squad_name(squad_string):
    """Given a fotmob squad name (from the url), returns a standardized squad name and the abbreviation"""

    squad_dict = {'ajax': 'AFC Ajax', 'az-alkmaar': 'AZ Alkmaar', 'fc-groningen': 'FC Groningen', 'fc-twente': 'FC Twente', 'fc-utrecht': 'FC Utrecht', 'feyenoord': 'Feyenoord', 'fortuna-sittard': 'Fortuna Sittard', 'go-ahead-eagles': 'Go Ahead Eagles', 'heracles': 'Heracles Almelo',
                  'nec-nijmegen': 'NEC Nijmegen', 'pec-zwolle': 'PEC Zwolle', 'psv-eindhoven': 'PSV', 'rkc-waalwijk': 'RKC Waalwijk', 'cambuur': 'SC Cambuur', 'sparta-rotterdam': 'Sparta Rotterdam', 'vitesse': 'Vitesse', 'willem-ii': 'Willem II', 'sc-heerenveen': 'sc Heerenveen'}
    name = squad_dict[squad_string]

    abbr_dict = {'AFC Ajax': 'aja', 'AZ Alkmaar': 'az', 'FC Groningen': 'gro', 'FC Twente': 'twe', 'FC Utrecht': 'utr', 'Feyenoord': 'fey', 'Fortuna Sittard': 'for', 'Go Ahead Eagles': 'gae', 'Heracles Almelo': 'her',
                 'NEC Nijmegen': 'nec', 'PEC Zwolle': 'pec', 'PSV': 'psv', 'RKC Waalwijk': 'rkc', 'SC Cambuur': 'cam', 'Sparta Rotterdam': 'spa', 'Vitesse': 'vit', 'Willem II': 'wil', 'sc Heerenveen': 'hee'}
    abbr = abbr_dict[name]

    return {'name': name, 'abbreviation': abbr}


def generate_hashtag_fotmob(url):
    """"""

    fm_string = url.split("/")[-1]
    home, away = fm_string.split("-vs-")
    home = standardize_squad_name(home)['abbreviation']
    away = standardize_squad_name(away)['abbreviation']

    return "#" + home + away


def get_mc_urls(url):
    # get the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    matchcard_urls = []

    # for field players
    lineup = soup.find_all(class_=re.compile("TeamContainer"))
    for squad in lineup:
        for rated_player_url in [a for a in squad.find_all('a') if 'match-card' in str(a)]:
            matchcard_urls.append(
                f"https://www.fotmob.com{rated_player_url['href']}")

    # for bench players
    for bench_item in soup.find_all(class_=re.compile("LeftBenchItemOuter")):
        if 'PlayerRating' in str(bench_item):
            matchcard_urls.append(
                f"https://www.fotmob.com{bench_item.find('a')['href']}")

    return matchcard_urls


def get_matchcard_variable_list(start_variables, urls):
    """
    DOCSTRING
    """

    variable_names = []

    for url in matchcard_urls:
        # scrape matchcards
        mc_page = requests.get(url)
        mc_soup = BeautifulSoup(mc_page.content, 'html.parser')

        # find variable names, and add new ones to the list
        overlay = mc_soup.find(class_=re.compile("BGOverlay"))
        # exclude the first element, as it is the 'Top stats' string
        rowcontainers = overlay.find_all(class_=re.compile("RowContainer"))[1:]
        for variable_name in [row.find('span').get_text() for row in rowcontainers]:
            if variable_name not in variable_names:
                variable_names.append(variable_name)

    return start_variables + variable_names


def get_fotmob_stats(html_overlay):
    """
    DOCSTRING
    """

    # get all stat rows except the first, as that is the 'Top stats' string
    rowcontainers = html_overlay.find_all(class_ = re.compile("RowContainer"))[1:]  
    return {rc.find_all('span')[0].get_text(): (rc.find_all('span')[1].get_text() if len(rc.find_all('span')) > 1 else 'NaN') for rc in rowcontainers}

if __name__ == "__main__":
    """
    Season level data
    - urls to fotmob match facts of all fixtures in this Eredivisie season
    """
    variable_names = []
    fotmob_df = pd.DataFrame()

    playing_rounds = generate_match_urls(last_playing_round=3)

    for fixture_report in tqdm(playing_rounds, desc='fixtures'):
        """
        Fixture level data:
        - match ids (ours + fotmob)
        - match cards with player rating and stats
        """

        # get identifiers for this fixture
        match_id = generate_hashtag_fotmob(fixture_report)
        fotmob_match_id = fixture_report.split("/")[-3]

        # find all matchcard urls on the page
        matchcard_urls = get_mc_urls(fixture_report)

        # create a list of all variable names that fotmob offers on its matchcards + a 'name' and 'hashtag' variable
        if len(variable_names) == 0:
            print('Generating variable list...')
            variable_names = get_matchcard_variable_list(start_variables=['hashtag', 'name'], urls=matchcard_urls)

        for matchcard in tqdm(matchcard_urls, desc='matchcards'):
            """
            Player level data
            """
            # create df for this player, to be appended to the master df
            matchcard_df = pd.DataFrame(columns=variable_names)

            # scrape page
            mc_page = requests.get(matchcard)
            mc_soup = BeautifulSoup(mc_page.content, 'html.parser')

            # 'zoom in' on the matchcard overlay, as the original webpage is still present in the complete HTML response
            overlay = mc_soup.find(class_=re.compile("BGOverlay"))

            # set variables that are not part of the main fotmob statistics
            matchcard_df.at[0, 'hashtag'] = match_id
            matchcard_df.at[0, 'name'] = overlay.find(class_=re.compile('PlayerName')).get_text()

            # scrape all other variables, and add them to the new df
            variables_dict = get_fotmob_stats(overlay)
            for k in variables_dict:
                matchcard_df.at[0, k] = variables_dict[k]

            # add mew data to master df
            fotmob_df = pd.concat([fotmob_df, matchcard_df], ignore_index=True)

    fotmob_df.to_pickle(f"{ROOT}/data/raw/fotmob.pkl")
