import pandas as pd

df = pd.read_csv('data/grades.csv', parse_dates=['date'])

previous_query = ""

# iterate over the grades df
for i, row in df.iterrows():

    # get query parameters
    fixture = row.hashtag
    fixture_date = row.date
    start_date = fixture_date + pd.DateOffset(-1)
    end_date = fixture_date + pd.DateOffset(1)
    start_date = start_date.date()
    end_date = end_date.date()

    # create the query
    query = f'snscrape --jsonl --progress --since {start_date} twitter-hashtag "#{fixture} until:{end_date}" > {fixture}.json'

    # remove double entries
    if query != previous_query:
        # write to txt file    
        with open('./res/twitter_scrape_queries.txt', 'a') as file:
            file.write(f"{query}\n")

        # update previous query
        previous_query = query