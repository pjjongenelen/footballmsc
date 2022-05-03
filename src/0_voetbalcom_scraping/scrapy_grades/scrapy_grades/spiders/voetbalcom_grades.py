"""
Scrapes all grade pages for the Eredivisie 2021-2022 so far.
Source: voetbal.com
"""

import pickle
import scrapy

ROOT = "C:/Users/timjo/python_projects/footballmsc"

class GradesSpider(scrapy.Spider):
    name = "grades"

    def start_requests(self):
        # get the urls for the rounds
        with open(f"{ROOT}/res/voetbalcom_match_report_urls_eredivisie_2122.pkl", "rb") as f:
            urls = pickle.load(f)

        for playing_round in urls:
            for url in playing_round:
                yield scrapy.Request(url="https://www.voetbal.com" + url + "noten/", callback=self.parse)

    def parse(self, response):
        fixture = response.url.split("/")[-3].split("2022-")[-1]
        filename = f"{fixture}-2122.html"
        with open(f"{ROOT}/data/raw/voetbalcom_html/{filename}", "wb") as f:
            f.write(response.body)