"""
DOCSTRING
"""

import eredivisie_nlp as enlp
import numpy as np
import pandas as pd
from pattern.nl import sentiment
from transformers import RobertaTokenizer, RobertaForSequenceClassification


# Zero-shot RobBERT:
# MODEL_CHOICE = 0
# RobBERT fine-tuned on 450 training samples:
MODEL_CHOICE = 1
# RobBERT fine-tuned on 900 training samples:
# MODEL_CHOICE = 2

# load model and tokenizer
if MODEL_CHOICE == 0:
    model = RobertaForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base")
elif MODEL_CHOICE == 1:
    model = RobertaForSequenceClassification.from_pretrained("./robbert_450")
elif MODEL_CHOICE == 2:
    model = RobertaForSequenceClassification.from_pretrained("./robbert_900")
else:
    raise ValueError(f"'{MODEL_CHOICE}' is not a valid option for MODEL_CHOICE. Please select a valid number.")
tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")


def get_score(score):
    """
    Converts model output scores {0:6} to SA floats {-0.9:0.9}

    :param score: RobBERT sentiment score between 0 and 6
    :returns: value between -0.9 (extremely negative) and 0.9 (extremely positive)
    """

    score_mapping = {
        0: -0.9,
        1: -0.6,
        2: -0.3,
        3: 0,
        4: 0.3,
        5: 0.6,
        6: -0.9
    }

    return score_mapping[score]


def annotate_tweets(tweet_pp_list):
    """
    DOCSTRING
    """

    tweet_sentiments = []
    for tweet_pp in tweet_pp_list:
        # list of sentiment scores per sentence for this tweet
        sentiments = []
        for sent in tweet_pp:
            # get sentiment scores from model
            t_sent = tokenizer(sent, return_tensors='pt')
            output = model(**t_sent)
            scores = output[0][0].detach().numpy()

            # get class label by selecting the max score
            label = np.where(scores == max(scores))[0].item()
            sentiments.append(get_score(label))

        tweet_sentiments.append(sentiments)

    return tweet_sentiments


# load tweets dataframe
# df = pd.read_pickle(f"{enlp.determine_root()}/data/tweets.pkl")

