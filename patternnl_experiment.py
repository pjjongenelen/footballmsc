import pandas as pd
import pattern
from pattern.nl import sentiment

# get a list of the contents of the tweets
tweets = pd.read_json("./data/nedtsj.json", lines=True).renderedContent.tolist()
scores = [-0.2, -0.6, 0, 0.2, 0, 0, -0.3, 0.3, -0.6, -0.1, 0, 0.3, -0.6, 0, -0.8, -0.2, -0.4, -0.1, 0.1, 0]

sentiments = []
for x in range(20):
    sentiments.append(sentiment(tweets[x])[0])

print(f"Average error of sentiment score: {sum([abs(sco - sen) for sco, sen in zip(scores, sentiments)])/20}")
print(pattern.__file__)


