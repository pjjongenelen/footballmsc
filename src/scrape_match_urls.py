from bs4 import BeautifulSoup
import pandas as pd
import pickle
import requests

N_PLAYING_ROUNDS = 23
ROOT = "C:/Users/timjo/PycharmProjects/footballmsc"
URLS = [f"https://www.voetbal.com/wedstrijdgegevens/ned-eredivisie-2021-2022-spieltag/{play_round}/" for play_round in range(1, 1 + N_PLAYING_ROUNDS)]

match_reports = []

# for each playing rounds
for url in URLS:
    mr = []
    # scrape the website, and get the correct table
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all('table')[1]

    # get all match report urls
    for tr in table.findAll("a"):
        if 'wedstrijdverslag' in tr['href']:
            mr.append(tr['href'])

    # store in master list
    match_reports.append(mr)

# save in the spiders folder for easy access later on
with open(f"{ROOT}/data/voetbalcom_match_report_urls_eredivisie_2122.pkl", "wb") as f:
    pickle.dump(match_reports, f)