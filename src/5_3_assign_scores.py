"""
DOCSTRING
"""

import numpy as np
import eredivisie_nlp as enlp
from tqdm import tqdm
import pandas as pd

# load data files
df = pd.read_pickle(f"{enlp.determine_root()}/data/master_annotations_with_teams.pkl")
grades = pd.read_csv(enlp.determine_root() + "/data/grades_with_teams.csv", index_col=[0])

# some further preprocessing specific to this code
# 1) lowercase gae
df['hashtag'] = df['hashtag'].str.lower()
# 2) add twitter columns to grades dataframe
grades['score_manual'] = np.NAN
grades['score_pattern'] = np.NAN
grades['num_tweets'] = np.NAN
grades['score_robbert'] = np.NAN

# get set of hashtags to iterate over
hashtags = [tag for tag in list(set(df.hashtag)) if tag in list(set(grades.hashtag))]

# keep track of dataset size per fixture
num_tweets = []

for hashtag in tqdm(hashtags):
    # get playing times
    start_time = pd.to_datetime(grades[grades.hashtag == hashtag].datetime.tolist()[0])
    end_time = start_time + pd.DateOffset(hours=1, minutes=50)  # we assume 5 minutes extra time

    # slice the dataframe on the start and end timestamps
    before = df.loc[(df.hashtag == hashtag) & (df.date < start_time)]
    during = df.loc[(df.hashtag == hashtag) & (df.date > start_time) & (df.date < end_time)]
    after = df.loc[(df.hashtag == hashtag) & (df.date > end_time)]

    # add number of tweets information to list
    num_tweets.append([before.shape[0], during.shape[0], after.shape[0]])

    # for this first version we'll only use the tweets from during the match
    df_slices = [during]

    # assign scores to players or to the match in general
    for subset in df_slices:
        # get set of player mentions
        mentions = set([p for player in during.players for p in player])

        # for each player
        for mention in mentions:
            # check if this player is in the grades dataframes
            grades_df_mention = grades.loc[(grades.hashtag == hashtag) & (grades.player_id == mention)]
            if grades_df_mention.shape[0] == 1:
                # add the two pattern-based scores
                for score in ['score_pattern', 'score_robbert', 'score_manual']:
                    # get the list of sentiment scores
                    mention_scores = [row[score] for _, row in subset.iterrows() if mention in row.players]
                    # calculate the average score and the number of mentions
                    avg_score = round(sum(mention_scores)/len(mention_scores), 1)
                    num_scores = len(mention_scores)
                    # add to the grades dataframe
                    grades.loc[(grades.hashtag == hashtag) & (grades.player_id == mention), score] = avg_score
                    grades.loc[(grades.hashtag == hashtag) & (grades.player_id == mention), 'num_tweets'] = num_scores

grades['num_tweets'] = [0 if np.isnan(nt) == True else nt for nt in grades['num_tweets']]

grades.to_pickle(enlp.determine_root() + "/data/grades+twitter.pkl")