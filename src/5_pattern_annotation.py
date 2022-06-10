"""
DOCSTRING
"""

import eredivisie_nlp as enlp
import pandas as pd
from pattern.nl import sentiment

REMOVED_STOPWORDS = False
if REMOVED_STOPWORDS:
    pickle = "tweets.pkl"
    save = "with"
else:
    pickle = "tweets_nostopw.pkl"
    save= "without"


df = pd.read_pickle(f"{enlp.determine_root()}/data/{pickle}")
content_pp = []
for tweet in df.text_pp:
    last_char = tweet[-1][-1]
    if last_char == "." or last_char == "!" or last_char == "?":
        content_pp.append(" ".join(tweet))
    else:
        content_pp.append(" ".join(tweet) + ".")

df['content_pp'] = content_pp
df['sentiment_pattern'] = [round(sentiment(tweet)[0], 1) for tweet in df['content_pp']]

sentences = pd.DataFrame({"text": df.content_pp, "hashtag": df.hashtag, "annotation": 100, "sentiment_pattern": df.sentiment_pattern})
options = {'strings_to_formulas': False, 'strings_to_urls': False}
writer = pd.ExcelWriter(f"{enlp.determine_root()}/data/sentiment_annotations_pattern_{save}_stopwords.xlsx", engine='xlsxwriter', options=options)
sentences.to_excel(writer, 'Sheet_1', index=False)
writer.save()
