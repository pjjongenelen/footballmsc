from asyncore import file_dispatcher
import glob, os
import pandas as pd
from tqdm import tqdm

# create list of json file locations
json_dir = 'data/raw/tweets_json'
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
df.to_pickle('data/tweets.pkl')