"""
TODO:
- replace player aliases with standardized names
- remove hashtags, tags, and URLs
"""

import emoji
import pandas as pd


ROOT = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"


def preprocessor(tweet):
    """
    Removes:
    - line breaks
    - double spaces

    Replaces:
    - emojis with text
    """

    # remove
    tweet = tweet.replace("\n", " ")
    while "  " in tweet:
        tweet = tweet.replace("  ", " ")

    # replace
    tweet = emoji.demojize(tweet)

    return tweet


if __name__ == "__main__":
    # load data, and get only the tweets
    df = pd.read_csv(f"{ROOT}/data/tweets.csv")
    tweets = df[df.lang == 'nl'].renderedContent.tolist()

    # ! Create development set
    tweets = tweets[:20]

    # apply preprocessor to all tweets
    preprocessed_tweets = list(map(preprocessor, tweets))


