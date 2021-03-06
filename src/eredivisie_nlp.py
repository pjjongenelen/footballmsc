"""
Collection of functions that are helpful for processing Eredivisie data
"""

import json
import pandas as pd
import platform
from unidecode import unidecode


def avg(array: list):
    return sum(array) / len(array)


def determine_root():
    if platform.node() == "DESKTOP-8K4NAR6":
        root = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"
    elif platform.node() == "Lenovo-TJ":
        root = "C:/Users/timjo/OneDrive - TU Eindhoven/Silva_Ducis/Scriptie/footballmsc"
    else:
        print('Unknown device. Please update the ROOT-path selector in the determine_root function.')

    return root


def fixture_tweets(hashtag: str) -> pd.DataFrame:
    """Returns all Dutch tweets for a given fixture"""

    # load all tweets
    tweets_df = pd.read_pickle(f"{determine_root()}/data/tweets.pkl")

    # return all Dutch tweets with this hashtag
    return tweets_df[(tweets_df.hashtag == hashtag) & (tweets_df.lang == 'nl')].reset_index(drop=True)


def simple_normalize(string):
    return unidecode(string).lower()


def home_and_away(hashtags: list):
    """ Given a list of hashtags, returns a list of the home teams and a list of the away teams """

    home_teams = []
    away_teams = []

    for hashtag in hashtags:
        # remove hashtag token
        hashtag = hashtag.replace("#", "")

        # split team abbreviations
        az_index = hashtag.find("az")
        if az_index == -1:
            # as was not playing this match
            home_teams.append(hashtag[:3])
            away_teams.append(hashtag[3:])
        elif az_index == 0:
            home_teams.append("az")
            away_teams.append(hashtag[2:])
        else:
            home_teams.append(hashtag[:3])
            away_teams.append("az")

    return home_teams, away_teams


def is_positive(number):
    if number == 0:
        return 0
    elif number > 0:
        return 1
    else:
        return -1


def round_score(number):
    return round(round(round(number, 1) / 3, 1) * 3, 1)


def transform_score(score, to='sentiment'):
    """
    Converts model output scores {0:6} to SA floats {-0.9:0.9}

    :param score: RobBERT sentiment score between 0 and 6
    :returns: value between -0.9 (extremely negative) and 0.9 (extremely positive)
    """
    if to == 'sentiment':
        score_mapping = {0: -0.9, 1: -0.6, 2: -0.3, 3: 0, 4: 0.3, 5: 0.6, 6: 0.9}
    elif to == 'robbert':
        score_mapping = {-0.9: 0, -0.6: 1, -0.3: 2, 0: 3, 0.3: 4, 0.6: 5, 0.9: 6}
    else:
        return "Please enter a valid value for the 'to' parameter."

    return score_mapping[score]
