import pandas as pd


# load data
df = pd.read_csv('data/players.csv', index_col = [0])
df = df.reset_index(drop=True)

# add seperate columns for first and last names
df['first_name'] = df.name.str.split().str[0]
df['last_name'] = df.name.str.split().str[1:].str.join(" ")

# save 
df.to_csv('data/players.csv')