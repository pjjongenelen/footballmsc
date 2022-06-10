"""
Preprocesses the Eredivisie players dataframe

Currently implemented:
- Split first and last name
- Add player IDs
- Replace special characters with general form - e.g., í > i and ç > c
"""

from unidecode import unidecode
import pandas as pd


ROOT = "C:/Users/timjo/OD/Silva_Ducis/Scriptie/footballmsc"


# load data
df = pd.read_csv(f'{ROOT}/data/players.csv', index_col=[0])
df = df.reset_index(drop=True)

# add separate columns for first and last names
first_names = []
last_names = []
for name_list in df.name.str.split(" "):
    if len(name_list) == 1:
        first_names.append('0')
        last_names.append(name_list[0])
    else:
        first_names.append(name_list[0])
        last_names.append(" ".join(name_list[1:]))

df['first_name'] = [unidecode(fn) for fn in first_names]
df['last_name'] = [unidecode(ln) for ln in last_names]
df['name'] = [unidecode(n) for n in df.name]

# add abbreviations of clubs
club_abbreviations = {'Ajax': 'aja', 'AZ Alkmaar': 'az', 'FC Groningen': 'gro', 'FC Twente': 'twe', 'FC Utrecht': 'utr', 'Feyenoord': 'fey', 'Fortuna Sittard': 'for', 'Go Ahead Eagles': 'gae', 'Heracles': 'her', 'NEC': 'nec', 'PEC Zwolle': 'pec', 'PSV': 'psv', 'RKC Waalwijk': 'rkc', 'SC Cambuur': 'cam', 'Sparta': 'spa', 'Vitesse': 'vit', 'Willem II': 'wil', 'SC Heerenveen': 'hee'}
df['squad_abbr'] = df['squad'].map(club_abbreviations)

# generate player IDs
df['player_id'] = df['last_name'].str.replace(" ", "").str.lower() + "_" + df['squad_abbr']

# save to disk
df.to_csv(f'{ROOT}/data/players.csv')