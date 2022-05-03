import os
import pandas as pd

df = pd.read_pickle(f"{os.getcwd()}/data/0_fotmob_scraping.pkl")
df = df.drop(['hashtag', 'name', ' FotMob rating'], axis=1)

perc_non_na = (1 - (df.isna().sum().sum() / (df.shape[0] * df.shape[1]))) * 100
print(f"{perc_non_na}% of the dataframe is data.")
print(f"That means we have on average, {len(df.columns) * 0.44698} fields per player.")
