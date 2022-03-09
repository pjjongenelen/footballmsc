"""
Scrapes all squad pages (players + position + value) for the Eredivisie 2021-2022 season
Source: transfermarkt.com
"""

import scrapy

ROOT = "C:/Users/timjo/python_projects/footballmsc"

class SquadSpider(scrapy.Spider):
    name = "squads"

    def start_requests(self):
        # create the correct urls to scrape
        teams = ['ajax-amsterdam', 'psv-eindhoven', 'feyenoord-rotterdam', 'az-alkmaar', 'vitesse-arnheim', 'fc-utrecht', 
        'sc-heerenveen', 'fc-groningen', 'fc-twente-enschede', 'heracles-almelo', 'willem-ii-tilburg', 'fortuna-sittard', 
        'pec-zwolle', 'sparta-rotterdam', 'nec-nijmegen', 'sc-cambuur-leeuwarden', 'rkc-waalwijk', 'go-ahead-eagles-deventer']
        ids = [610, 383, 234, 1090, 499, 200, 306, 202, 317, 1304, 403, 385, 1269, 468, 467, 133, 235, 1435]

        urls = [f'https://www.transfermarkt.com/{team}/kader/verein/{id}/saison_id/2021/plus/1' for team, id in zip(teams, ids)]

        # urls = [f"https://www.transfermarkt.com/{team}/startseite/verein/{id}/saison_id/2021" for team, id in zip(teams, ids)]
                
        # scrape the pages
        for squad in urls:
            yield scrapy.Request(squad, callback=self.parse)

    def parse(self, response):
        squad = response.url.split("/")[-8]
        # save to file
        filename = f"{squad}_2122.html"
        with open(f"{ROOT}/data/squads_html/{filename}", "wb") as f:
            f.write(response.body)
