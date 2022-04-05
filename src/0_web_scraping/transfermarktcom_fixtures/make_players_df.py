import os
import pandas as pd

ROOT = "C:/Users/timjo/python_projects/footballmsc"
COLUMN_NAMES = ['number', 'name', 'position', 'birthday', 'age', 'height', 'foot', 'joined', 'contract', 'value']
DFS = []

# for each squad
for html in os.listdir(f"{ROOT}/data/squads_html"):
    # get the squad name
    squad = html.split('_')[0].replace("-", " ")

    # get the dataframe with triplets
    df = pd.read_html(f"{ROOT}/data/squads_html/{html}")[1].copy()

    # creates a list of pandas series that can be concatenated into a dataframe for this squad
    series = []

    for index, data in df.iterrows():
        if index % 3 == 0:
            number = data['#']
            name = df['player'][index+1]
            position = df['player'][index+2]
            birthday = data['Date of birth / Age'].split('(')[0]
            age = data['Date of birth / Age'].split('(')[1][:2]
            height = data['Height'][:4].replace(',','')
            foot = data['Foot']
            joined = data['Joined']
            contract = data['Contract']
            if data['Market value'][-3:] == 'Th.':
                value = float(data['Market value'][1:-3]) * 1000
            elif data['Market value'][-1] == 'm':
                value = float(data['Market value'][1:-1]) * 1000000

            data = pd.Series([number, name, position, birthday, age, height, foot, joined, contract, value])
            series.append(data)

    new_df = pd.DataFrame(series)
    new_df.set_axis(COLUMN_NAMES, axis=1, inplace=True)
    new_df['squad'] = squad
    DFS.append(new_df)

all_squads_df = pd.concat(DFS)
all_squads_df.to_csv(f"{ROOT}/data/eredivisie_players_transfermarktcom.csv")