"""
Scrapes all player grades for the Eredivisie 2021-2022 season so far
Source: fotmob.com
"""

from bs4 import BeautifulSoup
import scrapy

ROOT = "C:/Users/timjo/python_projects/footballmsc"

class SquadSpider(scrapy.Spider):
    name = "fotmob_grades"

    def start_requests(self):
        # # create the correct urls to scrape
        # teams = ['ajax-amsterdam', 'psv-eindhoven', 'feyenoord-rotterdam', 'az-alkmaar', 'vitesse-arnheim', 'fc-utrecht', 
        # 'sc-heerenveen', 'fc-groningen', 'fc-twente-enschede', 'heracles-almelo', 'willem-ii-tilburg', 'fortuna-sittard', 
        # 'pec-zwolle', 'sparta-rotterdam', 'nec-nijmegen', 'sc-cambuur-leeuwarden', 'rkc-waalwijk', 'go-ahead-eagles-deventer']
        # ids = [610, 383, 234, 1090, 499, 200, 306, 202, 317, 1304, 403, 385, 1269, 468, 467, 133, 235, 1435]

        # urls = [f'https://www.transfermarkt.com/{team}/kader/verein/{id}/saison_id/2021/plus/1' for team, id in zip(teams, ids)]

        urls = ["https://www.fotmob.com/match/3602654/matchfacts/fc-groningen-vs-ajax"]
                
        # scrape the pages
        for squad in urls:
            yield scrapy.Request(squad, callback=self.parse)

    def parse(self, response):
        # transform to soup
        soup = BeautifulSoup(response.text, 'lxml')

        # get all player ratings from the field div
        field_rating_divs = soup.find_all("div", {"class": "css-oxmwlz-LineupPlayerRatingContainer"})
        field_ratings = [div.select("span")[0].text.strip() for div in field_rating_divs]
        print("RATINGS: -=-=-=-==-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print(field_ratings)

        # get all player ratings from the bench div
        # bench_section = soup.find_all("section", {"class": "css-1ovb10-BenchesContainer"})[0]
        print(response.css("section.css-1ovb10-BenchesContainer:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)").get())


        # get all player names to match the ratings

