"""
Merges the dataframes with grades and performance statistics acquired from FotMob.com and voetbal.com

Input: 0_fotmob_scraping.pkl, 0_voetbalcom_scraping.csv
Output: grades.csv
"""

from locale import normalize
import os
import pandas as pd
from pyparsing import col
import unidecode


def normalize_strings(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Given a column of strings:
    - removes special characters
    - converts to lowercase
    - removes leading and trailing spaces

    Keyword arguments:
    df -- the dataframe in question
    columns -- list of string column(s) to be normalized
    """

    for column in columns:
        # take note of how many unique values there are
        unique_strings = len(set(df[column]))

        # the actual processing steps
        df[column] = df[column].map(unidecode.unidecode)
        df[column] = df[column].str.lower()
        df[column] = df[column].str.strip()

        # check if we did not remove information from the column
        if len(set(df[column])) != unique_strings:
            raise Exception("Preprocessing column: {column} changed the amount of unique strings in the series.")

    return df


def main():
    # load data
    fotmob = pd.read_pickle(f"{os.getcwd()}/data/raw/grades/0_fotmob_scraping.pkl")
    voetbalcom = pd.read_csv(f"{os.getcwd()}/data/raw/grades/0_voetbalcom_scraping.csv", index_col=[0])

    # preprocess name strings
    fotmob = normalize_strings(fotmob, ['name'])
    voetbalcom = normalize_strings(voetbalcom, ['player'])

    # fix typos in names
    fotmob['name'] = fotmob['name'].replace({'dimitris siovas': 'dimitrios siovas', 'dimitrios limnios': 'dimitris limnios', 'eliazer dasa': 'eli dasa', 'francis ross': 'frank ross', 'giannis-fivos botos': 'giannis-foivos botos', 'hillary gong': 'hilary gong', 'iiass bel hassani': 'iliass bel hassani', 'ikoma lois openda': 'lois openda', 'jordan rolly botaka': 'jordan botaka', 'martjin berden': 'martijn berden', 'mitchel van bergen': 'mitchell van bergen', 'nikolai baden': 'nikolai baden frederiksen', 'ole ter haar romeny': 'ole romeny', 'philipp mwene': 'phillipp mwene', 'souffian elkarouani': 'souffian el karouani', 'tijani reijnders': 'tijjani reijnders', 'vinicius': 'carlos vinicius', 'evangelos pavlidis': 'vangelis pavlidis'})
    voetbalcom['player'] = voetbalcom['player'].replace({'anargyros kampetsis': 'argyris kampetsis', 'aslak witry': 'aslak fonn witry', 'dan crowley': 'daniel crowley', 'driess saddiki': 'dries saddiki', 'giannis botos': 'giannis-foivos botos', 'kwasi wriedt': 'kwasi okyere wriedt', 'marcus pedersen': 'marcus holmgren pedersen', 'maxi romero': 'maximiliano romero', 'mica pinto': 'michael pinto', 'mo el hankouri': 'mohamed el hankouri', 'nico tagliafico': 'nicolas tagliafico', 'nikos michelis': 'nikolaos michelis', 'othmane boussaid': 'othman boussaid', 'sijb van ottele': 'syb van ottele', 'ulrik jenssen': 'ulrik yttergard jenssen', 'dalmau': 'adrian dalmau', 'andre ramalho': 'andre ramalho silva', 'cordoba': 'inigo cordoba'})
    
    # create id column to merge on
    fotmob['id'] = fotmob.name + fotmob.hashtag
    voetbalcom['id'] = voetbalcom.player + "#" + voetbalcom.hashtag

    # remove excess columns from voetbal.com df
    voetbalcom.drop(['Ø', 'match_id'], axis=1, inplace=True)

    # merge dataframes
    df = pd.merge(voetbalcom, fotmob, on='id', how='outer')

    # resolve duplicate columns: player names and hashtags
    df['hashtag'] = [tag_y if isinstance(tag_y, str) else tag_x for tag_x, tag_y in zip(df.hashtag_x, df.hashtag_y)]
    df['player'] = [n1 if isinstance(n1, str) else n2 for n1, n2 in zip(df.player, df.name)]
    df.drop(['hashtag_x', 'hashtag_y', 'name', 'club'], axis=1, inplace=True)

    # save to disk
    df.to_csv(f"{os.getcwd()}/data/raw/grades/grades_raw.csv")
    

if __name__ == '__main__':
    main()