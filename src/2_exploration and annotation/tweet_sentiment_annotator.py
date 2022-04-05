import pandas as pd
from sklearn.utils import shuffle
import time

ROOT = "C:/Users/timjo/python_projects/footballmsc"

# load data and get list of tweets that still have to be annotated
df = pd.read_csv(f"{ROOT}/data/only_tweets.csv", index_col = [0])
start = time.time()
already_annotated = df[df.annotation != 100].shape[0]

for index, row in shuffle(df).iterrows():
    if row.annotation == 100:
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        print(row.content)

        annotation = input()
        if annotation == "!":
            break

        annotation = int(annotation)
        df.at[index, 'annotation'] = annotation

# save to csv
print(f"Annotated {df[df.annotation != 100].shape[0] - already_annotated} items in {round((time.time() - start) / 60)} minutes.")
df.to_csv(f'{ROOT}/data/only_tweets.csv')