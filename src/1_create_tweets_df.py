import glob
import os
import pandas as pd
from tqdm import tqdm


ROOT = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"


# create list of json file locations
json_dir = f'{ROOT}/data/raw/tweets_json'
json_pattern = os.path.join(json_dir, "*.json")
file_list = glob.glob(json_pattern)

# create main dataframe of tweets
dfs = []

files_progress = tqdm(file_list)
for file in files_progress:
    # set progress bar
    files_progress.set_description("Processing json files")

    # load file
    with open(file) as f:
        json_data = pd.read_json(file, lines=True)

    # add hashtag info
    json_data['hashtag'] = "#" + file.split("\\")[-1].split(".")[0]

    dfs.append(json_data)

# make main df and save to pickle
df = pd.concat(dfs)
df = df.reset_index(drop=True)
df.to_pickle(f'{ROOT}/data/tweets.pkl')