"""
Generates a JSON file that contains a many-to-one mapping of strings to Eredivisie players.
The 'one' part of this mapping is the player id (LASTNAME_squad; 'Maarten Stekelenburg' > 'STEKELENBURG_aja'.).

Implemented aliases:
- Twitter usernames
- Unique first and last names
- Full name

TODO:
- Typos
"""
# %%

import json
import pandas as pd


ROOT = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"


# load the data and create the alias dictionary
df = pd.read_csv(f"{ROOT}/data/players.csv", index_col=[0])
alias_dict = {}

# twitter usernames
twitter_dict = {twitter: player for twitter, player in zip(
    df.twitter, df.player_id) if twitter != "-"}
alias_dict = alias_dict | twitter_dict

# unique first names
unique_first_names = {name: player for name, player in zip(
    df.first_name, df.player_id) if df.first_name.tolist().count(name) == 1}
alias_dict = alias_dict | unique_first_names

# unique last names
unique_last_names = {name: player for name, player in zip(
    df.last_name, df.player_id) if df.last_name.tolist().count(name) == 1}
alias_dict = alias_dict | unique_last_names

# full name
full_names = {name: player for name, player in zip(df.name, df.player_id)}
alias_dict = alias_dict | full_names

# group the dictionary entries per squad
squads = [alias_dict[key].split('_')[1] for key in alias_dict]
final_dict = {}
for squad, entry in zip(squads, alias_dict):
    if squad in final_dict.keys():
        final_dict[squad][entry] = alias_dict[entry]
    else:
        final_dict[squad] = {entry: alias_dict[entry]}

# save to disk
with open(f"{ROOT}/data/aliases.json", "w") as f:
    json.dump(final_dict, f, indent=4)
