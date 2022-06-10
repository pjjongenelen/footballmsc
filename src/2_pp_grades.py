"""
Preprocessing of the grades dataframe
Steps:
- Convert grade columns to float

Input: data/raw/grades/grades.csv
Output: data/grades.csv
"""

import eredivisie_nlp as enlp
import numpy as np
import pandas as pd


def preprocess_grades_column(col: pd.Series) -> pd.Series:
    """
    Turns grade columns from mixture of str and float into all float
    :param col: column with player grades
    :returns: col as float with missing values as np.NaN
    """

    # recode missing values to NaN
    col = col.astype('str')
    col.replace({'nan': np.nan, '---': np.nan}, inplace=True)

    # change string numbers to float
    col = col.astype('float')

    return col


def convert_datetime(grades):
    """
    Converts date and time columns to pandas datetime format.
    Pandas timezone (tz) functions only work on dataframes where the datetime information is in the index.
    Therefore, we set and reset the index in the procedure below.

    :param grades: entire grades dataframe
    :returns: input grades dataframe with new column containing UTC datetime stamps
    """

    # join strings
    grades['datetime'] = grades.date + " " + grades.time
    # convert to datetime
    grades.datetime = pd.to_datetime(grades.datetime)
    # convert CET to UTC
    grades = grades.set_index('datetime')
    grades.index = grades.index.tz_localize('CET')
    grades.index = grades.index.tz_convert('UTC')
    grades = grades.reset_index()

    return grades


def get_ids(grades):
    """
    Creates
    :param grades: entire grades dataframe
    :return: list of player ids
    """

    # read players dataframe
    players = pd.read_csv(enlp.determine_root() + "/data/players.csv", index_col=[0])
    # convert player names to lowercase voor vlookup
    players['player'] = [n.lower() for n in players.name]
    # add squad info + player ids to grades df
    grades = pd.merge(grades, players[['player', 'squad_abbr', 'player_id']], on='player', how='left')
    # remove players that are in grades, but not in players
    grades = grades[~grades.squad_abbr.isna()]

    return grades


if __name__ == '__main__':
    # load data
    grades_df = pd.read_csv(f"{enlp.determine_root()}/data/raw/grades/grades_raw.csv", index_col=[0])

    # fix column names
    grades_df.rename(columns={' FotMob rating': 'FM'}, inplace=True)

    # preprocess grade columns
    for grade_column in ['AD', 'VI', 'FM']:
        grades_df[grade_column] = preprocess_grades_column(grades_df[grade_column])

    # only use the rows for which we have both fotmob and ad/vi grades
    grades_df = grades_df[grades_df['AD'].notna()]

    # convert date and time columns to pandas datetime format
    grades_df = convert_datetime(grades_df)

    # recode id column to use standardized format
    grades_df = get_ids(grades_df)

    # save to disk
    grades_df.to_csv(f"{enlp.determine_root()}/data/grades.csv")
