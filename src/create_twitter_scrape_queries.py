import pandas as pd

df = pd.read_csv('/data/grades.csv')

# get fixture info
fixture = 'ajapsv'
fixture_date = '2020_12_04'

start_date = fixture_date# - 1
end_date = fixture_date# + 1
query = f'snscrape --jsonl --progress --since {start_date} twitter-hashtag "#{fixture} until:{end_date}" > {fixture}.json'

print(query)

# with open('./res/twitter_scrape_queries.txt', 'a') as file:
#     file.write(query)