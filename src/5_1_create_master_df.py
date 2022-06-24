"""
Merge the multiple Excel files into one master dataframe:
- sentiment_annotations_with_stopwords.xlsx
- sentiment_annotations_without_stopwords.xlsx
- sentiment_annotations_no_leakage.xlsx

"""

import eredivisie_nlp as enlp
import numpy as np
import pandas as pd
from random import randint
from tqdm import tqdm
from transformers import RobertaForSequenceClassification, RobertaTokenizer

ann_path = f"{enlp.determine_root()}/data/sentiment_annotations"


def merge_source_dfs():
    """
    DOCSTRING
    :return:
    """

    print("Loading source data")
    df_p_s = pd.read_excel(io=f"{ann_path}_pattern_with_stopwords.xlsx", sheet_name='Sheet_1')
    df_man = pd.read_excel(io=f"{ann_path}_manual_no_leakage.xlsx", sheet_name='Sheet_1')
    df_robbert = pd.read_pickle(enlp.determine_root() + "/data/robbert_annotations.pkl").reset_index(drop=True)

    print("Merging dataframes")
    return pd.DataFrame({
        'text': df_man.text,
        'score_pattern': df_p_s.sentiment_pattern,
        'score_manual': [ann if ann != 100 else np.NaN for ann in df_man.annotation],
        'score_robbert': df_robbert.robbert
    })


if __name__ == "__main__":
    # load data
    df = merge_source_dfs()
    tweets = pd.read_pickle(enlp.determine_root() + "/data/tweets.pkl")

    # add hashtags to master df
    print("Adding hashtag column")
    df['hashtag'] = tweets.hashtag
    df['date'] = tweets.date

    # save to disk
    print("Saving to disk")
    df.to_pickle(f"{enlp.determine_root()}/data/master_annotations.pkl")
