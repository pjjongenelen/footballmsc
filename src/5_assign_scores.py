"""
DOCSTRING
"""

import numpy as np
import eredivisie_nlp as enlp
from tqdm import tqdm
import pandas as pd

# load data files
df = pd.read_pickle(f"{enlp.determine_root()}/data/master_annotations.pkl")
grades = pd.read_csv(enlp.determine_root() + "/data/grades.csv", index_col=[0])

# some further preprocessing specific to this code
# 1) add players column to twitter dataframe containing all player mentions
players = []
for text in df.text_no_s:
    tokenized = text.split()
    token_players = []
    for token in tokenized:
        if "_" in token and ":" not in token:
            # resolve small preprocessing bug with if statement
            if token[-1] in [".", "!", "?"]:
                token_players.append(token[:-1])
            else:
                token_players.append(token)
    players.append(token_players)
df['players'] = players
# 2) lowercase gae
df['hashtag'] = df['hashtag'].str.lower()
# 3) add twitter columns to grades dataframe
grades['score_m'] = np.NAN
grades['score_p_s'] = np.NAN
grades['score_p_no_s'] = np.NAN
grades['num_tweets'] = np.NAN

# get set of hashtags to iterate over
hashtags = [tag for tag in list(set(df.hashtag)) if tag in list(set(grades.hashtag))]

for hashtag in tqdm(hashtags):
    # get playing times
    start_time = pd.to_datetime(grades[grades.hashtag == hashtag].datetime.tolist()[0])
    end_time = start_time + pd.DateOffset(hours=1, minutes=50)  # we assume 5 minutes extra time

    # slice the dataframe on the start and end timestamps
    before = df.loc[(df.hashtag == hashtag) & (df.date < start_time)]
    during = df.loc[(df.hashtag == hashtag) & (df.date > start_time) & (df.date < end_time)]
    after = df.loc[(df.hashtag == hashtag) & (df.date > end_time)]
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
                for score in ['score_p_s', 'score_p_no_s']:
                    # get the list of sentiment scores
                    mention_scores = [row[score] for i, row in subset.iterrows() if mention in row.players]
                    # calculate the average score and the number of mentions
                    avg_score = round(sum(mention_scores)/len(mention_scores), 1)
                    num_scores = len(mention_scores)
                    # add to the grades dataframe
                    grades.loc[(grades.hashtag == hashtag) & (grades.player_id == mention), score] = avg_score
                    grades.loc[(grades.hashtag == hashtag) & (grades.player_id == mention), 'num_tweets'] = num_scores
                    
grades.to_pickle(enlp.determine_root() + "/data/grades+twitter.pkl")