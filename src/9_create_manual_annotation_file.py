"""
Code to set up the data for manually annotating sentences with a corresponding sentiment score.
Sentiment score is one of {-1, -0.9, -0.6, -0.3, 0, 0.3, 0.6, 0.9, 1}.

Output format (.xlsx):
| some_ID | sentence                         |
| 1       | well this wasn't great           |
| 2       | what a fantastic goal by Antony! |
| ...     | ...                              |

Result after manual coding:
| some_ID | sentiment score | sentence                         |
| 1       | -0.3            | well this wasn't great           |
| 2       | 0.9             | what a fantastic goal by Antony! |
| ...     | ...             | ...                              |
"""

import eredivisie_nlp as enlp
import pandas as pd

df = pd.read_pickle(f"{enlp.determine_root()}/data/tweets.pkl")
content_pp = []
for tweet in df.text_pp:
    last_char = tweet[-1][-1]
    if last_char == "." or last_char == "!" or last_char == "?":
        content_pp.append(" ".join(tweet))
    else:
        content_pp.append(" ".join(tweet) + ".")

df['content_pp'] = content_pp

# DONT RUN THE CODE BELOW, AS IT WILL OVERWRITE THE EXISTING EXCEL FILE, NAME IS ALREADY CHANGED FOR SAFETY

sentences = pd.DataFrame({"text": df.content_pp, "hashtag": df.hashtag, "annotation": 100})
options = {'strings_to_formulas': False, 'strings_to_urls': False}
writer = pd.ExcelWriter(f"{enlp.determine_root()}/data/sentiment_annotations_EMPTY.xlsx", engine='xlsxwriter', options=options)
sentences.to_excel(writer, 'Sheet_1', index=False)
writer.save()
