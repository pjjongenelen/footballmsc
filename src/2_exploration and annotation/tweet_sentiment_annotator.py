import pandas as pd
import random

ROOT = "C:/Users/timjo/python_projects/footballmsc"


def print_bars():
    print("-------------------------------------------------------")
    print("-----------------------------------------")
    print("-------------------------")
    print("---------")


# load data and get list of tweets that still have to be annotated
df = pd.read_csv(f"{ROOT}/data/only_tweets.csv", index_col = [0])
todo = df.index[df.annotation == 100].tolist()


for _ in todo:
    # get a random tweet to annotate
    index = random.sample(todo, 1)
    print(df.iloc[index]['content'].values[0])
    annotation = input()

    if annotation == "!":
        # stop annotating and save the file
        break

    elif annotation in [-2, -1, 0, 1]:
        # correct encoding, no typo
        df.loc[index,'annotation'] = annotation
        print_bars()


# save to csv
df.to_csv(f'{ROOT}/data/only_tweets.csv')