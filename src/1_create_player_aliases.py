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

import eredivisie_nlp as enlp
import json
import pandas as pd


# load the data and create the alias dictionary
df = pd.read_csv(f"{enlp.determine_root()}/data/players.csv", index_col=[0])
alias_dict = {}

# Twitter usernames
twitter_dict = {enlp.simple_normalize(twitter).lower(): enlp.simple_normalize(player) for twitter, player in zip(df.twitter, df.player_id) if twitter != "-"}
alias_dict = alias_dict | twitter_dict

# unique first names
unique_first_names = {enlp.simple_normalize(name): enlp.simple_normalize(player) for name, player in zip(df.first_name, df.player_id) if df.first_name.tolist().count(name) == 1}
alias_dict = alias_dict | unique_first_names

# unique last names
unique_last_names = {enlp.simple_normalize(name): enlp.simple_normalize(player) for name, player in zip(df.last_name, df.player_id) if df.last_name.tolist().count(name) == 1}
alias_dict = alias_dict | unique_last_names

# full names
full_names = {enlp.simple_normalize(name): enlp.simple_normalize(player) for name, player in zip(df.name, df.player_id)}
alias_dict = alias_dict | full_names

# manual insertions
manual = {'vindahl jensen': 'vindahl_az'}
alias_dict = alias_dict | manual

# manual deletions
del alias_dict['min']
del alias_dict['dan']

# create a JSON file with all alias mappings
with open(f"{enlp.determine_root()}/data/aliases.json", "w") as f:
    json.dump({'twitter': twitter_dict, 'name': full_names | unique_first_names | unique_last_names}, f, indent=4)

# create a JSON file that is grouped per club
grouped_per_club = {}
squads = [alias_dict[key].split('_')[1] for key in alias_dict]
for s in set(squads):
    grouped_per_club[s] = {'twitter': {}, 'name': {}}
# fill final_dict
for squad, entry in zip(squads, alias_dict):
    if entry[0] == '@':
        # if Twitter username
        grouped_per_club[squad]['twitter'][entry] = alias_dict[entry]
    else:
        # if natural name
        grouped_per_club[squad]['name'][entry] = alias_dict[entry]

# save to disk
with open(f"{enlp.determine_root()}/data/aliases_per_club.json", "w") as f:
    json.dump(grouped_per_club, f, indent=4)


