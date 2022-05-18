import pandas as pd
from sklearn.utils import shuffle
import time

ROOT = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"
FILE_TO_ANNOTATE = f"{ROOT}/data/temp/antony_ajapsv.csv"


# load data and get list of tweets that still have to be annotated
df = pd.read_csv(FILE_TO_ANNOTATE, index_col = [0])

# create annotation column if necessary
if 'annotation' not in df.columns:
    df['annotation'] = 100

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
        
        try:
            annotation = float(annotation)
        except ValueError:
            # save for safety
            df.to_csv(f'{ROOT}/data/only_tweets.csv')
            # try to get valid input this time
            print("ERRONEOUS INPUT, PLEASE TRY AGAIN")
            annotation = input()

        df.at[index, 'annotation'] = annotation

# save to csv
print(f"Annotated {df[df.annotation != 100].shape[0] - already_annotated} items in {round((time.time() - start) / 60)} minutes.")
df.to_csv(FILE_TO_ANNOTATE)