import os
import pandas as pd

ROOT = "C:/Users/timjo/PycharmProjects/footballmsc"

def process_timestamp(timestamp: str):
    time = timestamp[-9:-4]
    date = timestamp.split(", ")[1][:-9].replace(".", "")
    return time, date

for html_file in os.listdir(f"{ROOT}/data/grades_html"):
    loc = ROOT + "/data/grades_html/" + html_file
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
        df2['fixture'] = home_club + " - " + away_club
        df2['time'], df2['date'] = process_timestamp(tables[2].columns[1])

        if home_club == "AFC Ajax" and away_club == "AZ Alkmaar":
            # create main df for first fixture
            df = df2.copy()
        else:
            # conatenate with main df
            df = pd.concat([df, df2], ignore_index=True)

# De Telegraaf has no published grades for this season on voetbal.com
df = df.drop('De Telegraaf', axis=1)

# save
df.to_csv(f"{ROOT}/data/voetbalcom_grades.csv")