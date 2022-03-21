"""
The snscrape package is run from the Anaconda prompt.
In order to scrape the tweets for all 206 matches in our sample, we need 206 queries (1 hashtag per query).
This script generates the 206 lines, and puts them in res/twitter_scrape_queries.txt.
Simply copying all these lines, and pasting them in an Anaconda prompt (with snscrape installed) will do the trick for data collection.
"""

# imports
import pandas as pd


# functions for readability
def make_query(df_row):
    """Returns a query for the fixture contained in df_row"""

    # get query parameters
    fixture = df_row.hashtag
    fixture_date = df_row.date

    # we scrape 1 day before, and 1 day after match
    start_date = fixture_date + pd.DateOffset(-1)
    end_date = fixture_date + pd.DateOffset(1)
    # remove hour-and-minute information
    start_date = start_date.date()
    end_date = end_date.date()

    return f'snscrape --jsonl --progress --since {start_date} twitter-hashtag "#{fixture} until:{end_date}" > {fixture}.json'

def main():
    """Fill res/twitter_scrape_queries.txt with the correct 206 queries"""

    # load data
    df = pd.read_csv('data/grades.csv', parse_dates=['date'])  # load dataframe that contains all fixtures
    
    # dummy variable to prevent duplicate queries
    previous_query = ""

    # main loop
    for _, row in df.iterrows():
        # get query for match
        query = make_query(row)

        # prevent double entries
        if query != previous_query:
            # write to txt file    
            with open('./res/twitter_scrape_queries.txt', 'a') as file:
                file.write(f"{query}\n")

            previous_query = query

if __name__ == "__main__":
    main()