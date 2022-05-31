"""
Tweet preprocessing algorithm

- replaces player aliases with standardized names
- removes urls
- tokenizes on a sentence level
- resolves hashtags
- #TODO remove mentions and non-alphanumerics
"""

import emoji
import eredivisie_nlp as enlp
import json
from nltk.tokenize import sent_tokenize
import pandas as pd
import re
from tqdm import tqdm


def trim_spaces(string):
    """
    Removes double, leading, and trailing spaces
    """

    # double spaces
    while "  " in string:
        string = string.replace("  ", " ")

    # leading and trailing
    string = string.strip()

    return string


def remove_and_replace(tweet):
    """
    Some basic steps that are grouped to keep the code clean, but do not deserve their own function.
    """

    # remove line breaks
    tweet = tweet.replace("\n", " ")
    # remove URLs
    tweet = re.sub(r'https?://(www\.)?[-a-zA-Z\d@:%._+~#=]{1,256}\.[a-zA-Z\d()]{1,6}\b([-a-zA-Z\d()@:%_+.~#?&/=]*)', "", tweet)
    # remove redundant whitespace
    tweet = trim_spaces(tweet)
    # replace emojis with text
    tweet = emoji.demojize(tweet)
    # apply sentence splitter
    tweet = sent_tokenize(tweet)
    # convert to lowercase
    tweet = [sent.lower() for sent in tweet]

    return tweet

def resolve_aliases(tweets, hashtags):
    """
    Replaces user mentions and names within the tweets with the standardized names
    Note that the input tweets need to be sentence tokenized

    :param tweets:   list of tweets as string
    :param hashtags: list of corresponding fixture hashtags
    :returns:        list of tweets where variants of player names are standardized into LASTNAME_squad
    """

    with open(f"{enlp.determine_root()}/data/aliases_per_club.json") as f:
        alias_dict = json.load(f)

    new_tweets = []
    for tweet, hashtag in tqdm(zip(tweets, hashtags), total=len(tweets)):

        # get only the dictionaries for the teams that were playing
        home, away = enlp.home_and_away([hashtag])[0][0].lower(), enlp.home_and_away([hashtag])[1][0].lower()
        alias_dictionaries = [alias_dict[home]['twitter'], alias_dict[home]['name'],
                              alias_dict[away]['twitter'], alias_dict[away]['name']]

        new_tweet = []
        for sent in tweet:
            for dictionary in alias_dictionaries:
                """Main loop per tweet, this section searches for alias occurrences in each of the sentences. Once 
                found, all aliases are stored in 'found_aliases', and we take the longest of them. This is because 
                aliases are nested - i.e., "FIRST LAST" will be matched to "FIRST LAST", "FIRST", and "LAST". Once 
                we've found the longest occurring alias in the sentence, we replace it with its standard form. """
                found_aliases = []

                for key, value in dictionary.items():
                    if key in sent:
                        found_aliases.append(key)

                if len(found_aliases) > 0:
                    key = max(found_aliases, key=len).lower()
                    sent = sent.replace(key, dictionary[key])

            # ensure output tweets are still sentence tokenized
            new_tweet.append(sent)

        new_tweets.append(new_tweet)

    return new_tweets


def remove_trailing_hashtags(tweets):
    """"
    Removes trailing hashtags from tweets, as we already have this info in the 'hashtags' column.

    This is an example tweet #python #football #letsgo
    Becomes:
    This is an example tweet

    :param tweets: pd.Series of tweets, sentence tokenized
    :returns:      list of tweets, sentence tokenized, without trailing hashtags
    """

    new_tweets = []
    for tweet in tqdm(tweets, desc="trailing hts"):
        new_tweet = []
        for sent in tweet:
            tokens = sent.split(" ")
            hashtag_index = None
            for index, text in reversed(list(enumerate(tokens))):
                if text[0] == "#":
                    hashtag_index = index
                else:
                    break

            # if the whole sentence consists of hashtags
            if hashtag_index == 0:
                pass
            else:
                # if we have trailing tags
                if hashtag_index:
                    sent = " ".join(tokens[:hashtag_index])
                new_tweet.append(sent)

        new_tweets.append(new_tweet)

    return new_tweets


def resolve_in_text_hashtags(tweets):
    """"
    Resolves in-text hashtags from tweets, as we already have this info in the 'hashtags' column and
    it will likely hamper the model's performance.

    This #thesis project uses a lot of #python code
    Becomes:
    This thesis project uses a lot of python code

    :param tweets: pd.Series of tweets, sentence tokenized
    :returns:      list of tweets, sentence tokenized, without trailing hashtags
    """

    new_tweets = []
    for tweet in tqdm(tweets, desc="in-text hts"):
        new_tweet = []
        for sent in tweet:
            sent = sent.replace("#", "")
            new_tweet.append(sent)
        new_tweets.append(new_tweet)

    return new_tweets


if __name__ == "__main__":
    # load data, and maintain only Dutch tweets
    df = pd.read_pickle(f"{enlp.determine_root()}/data/raw/tweets_raw.pkl")
    df = df[df.lang == 'nl'].reset_index(drop=True)

    # preprocess tweet text
    print("1/6 Replacing emojis, double spaces, and sentence tokenizing.")
    df['text_pp'] = list(map(remove_and_replace, df.content.tolist()))

    # remove redundant columns
    df.source = df.sourceLabel
    df.drop(['_type', 'url', 'renderedContent', 'lang', 'sourceUrl', 'sourceLabel',
                    'tcooutlinks', 'quotedTweet', 'inReplyToTweetId', 'inReplyToUser',
                    'mentionedUsers', 'coordinates', 'place', 'cashtags'], axis=1, inplace=True)

    # set home and away teams
    print("2/6 Adding home and away teams")
    df['home'], df['away'] = enlp.home_and_away(df.hashtag)

    # transform mentions and names to the standardized name format
    print("3/6 Resolving aliases")
    df.text_pp = resolve_aliases(df.text_pp, df.hashtag)

    # deal with hashtags
    print("4/6 Working on hashtags")
    df.text_pp = remove_trailing_hashtags(df.text_pp)
    df.text_pp = resolve_in_text_hashtags(df.text_pp)

    # remove mentions
    print("5/6 Replacing mentions with 'USER'")
    df.text_pp = [[re.sub(r'@\S+', "USER", sent) for sent in tweet] for tweet in df.text_pp]

    # remove non-alphanumerics and other special cases
    print("6/6 Replacing alphanumerics with corresponding text.")
    to_recode = {" & ": " en "}
    for key, value in to_recode.items():
        df.text_pp = [[sent.replace(key, value) for sent in tweet] for tweet in df.text_pp]

    # save to disk
    print("Saving to disk")
    df.to_pickle(f"{enlp.determine_root()}/data/tweets.pkl")