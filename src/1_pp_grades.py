"""
Preprocessing of the grades dataframe
Steps:
- Convert grade columns to float

Input: data/raw/grades/grades.csv
Output: data/grades.csv
"""

import numpy as np
import os
import pandas as pd


def preprocess_grades_column(col: pd.Series) -> pd.Series:
    """Turns grade columns from mixture of str and float into all float"""

    # recode missing values to NaN
    col = col.astype('str')
    col.replace({'nan': np.nan, '---': np.nan}, inplace=True)

    # change string numbers to float
    col = col.astype('float')

    return col



if __name__ == '__main__':
    # load data
    grades_df = pd.read_csv(f"{os.getcwd()}/data/raw/grades/grades_raw.csv", index_col=[0])

    # fix column names
    grades_df.rename(columns={' FotMob rating': 'FM'}, inplace=True)

    # preprocess grade columns
    for grade_column in ['AD', 'VI', 'FM']:
        grades_df[grade_column] = preprocess_grades_column(grades_df[grade_column])
    
    # save to disk
    grades_df.to_csv(f"{os.getcwd()}/data/grades.csv")