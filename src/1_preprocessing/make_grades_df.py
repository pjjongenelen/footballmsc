import os
import pandas as pd

ROOT = "C:/Users/timjo/python_projects/footballmsc"

def process_timestamp(timestamp: str):
    time = timestamp[-9:-4]
    date = timestamp.split(", ")[1][:-9].replace(".", "")
    return time, date

for html_file in os.listdir(f"{ROOT}/data/raw/voetbalcom_html"):
    loc = ROOT + "/data/raw/voetbalcom_html/" + html_file
    with open(loc, "rb") as f:
        # load the info from this html file
        tables = pd.read_html(f)
        home = tables[4]
        away = tables[5]

        # fix some columns
        home_club = home.columns[0]
        home['club'] = home_club
        home = home.rename(columns={home.columns[0]: "player"})
        away_club = away.columns[0]    
        away['club'] = away_club    
        away = away.rename(columns={away.columns[0]: "player"})

        # concatenate the dataframes
        df2 = pd.concat([home, away], ignore_index=True)

        # add general match info
        df2['home'] = home_club
        df2['away'] = away_club
        df2['time'], df2['date'] = process_timestamp(tables[2].columns[1])

        if home_club == "AFC Ajax" and away_club == "AZ Alkmaar":
            # create main df for first fixture
            df = df2.copy()
        else:
            # conatenate with main df
            df = pd.concat([df, df2], ignore_index=True)

# De Telegraaf has no published grades for this season on voetbal.com
df = df.drop('De Telegraaf', axis=1)

# We don't need the team averages per match, we can calculate this manually later
df.drop(df[df['player'] == "Team Ø"].index, inplace=True)
df.reset_index(drop=True)

# Add a column with the fixture hashtag
abbreviations = {'AFC Ajax': 'aja', 'AZ Alkmaar': 'az', 'FC Groningen': 'gro', 'FC Twente': 'twe', 'FC Utrecht': 'utr', 'Feyenoord': 'fey', 'Fortuna Sittard': 'for', 'Go Ahead Eagles': 'GAE', 'Heracles Almelo': 'her', 'NEC Nijmegen': 'nec', 'PEC Zwolle': 'pec', 'PSV': 'psv', 'RKC Waalwijk': 'rkc', 'SC Cambuur': 'cam', 'Sparta Rotterdam': 'spa', 'Vitesse': 'vit', 'Willem II': 'wil', 'sc Heerenveen': 'hee'}
df['hashtag'] = df.home.map(abbreviations) + df.away.map(abbreviations)

def map_substring(s, dict_map):
    for key in dict_map.keys():
        if key in s: 
            return dict_map[key]

# Transform date column to datetime type
months_map = {'Augustus': 'august', 'Oktober': 'october', 'November': 'november', 'December': 'december', 'Januari': 'january', 'Februari': 'february', 'Maart': 'march'}
for key in months_map:
    df.date = df.date.str.replace(key, months_map[key])
df.date = pd.to_datetime(df.date, infer_datetime_format=True)

# Add an ID for each match


# save
df.to_csv(f"{ROOT}/data/grades.csv", index=False)