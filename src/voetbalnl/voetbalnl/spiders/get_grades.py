import pickle
import scrapy

ROOT = "C:/Users/timjo/PycharmProjects/footballmsc"

class GradesSpider(scrapy.Spider):
    name = "grades"

    def start_requests(self):
        # get the urls for the first two rounds
        with open(f"{ROOT}/data/voetbalcom_match_report_urls_eredivisie_2122.pkl", "rb") as f:
            urls = pickle.load(f)

        for playing_round in urls:
            for url in playing_round:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("ZO ZIET LOGGEN ERUIT JONGUH!!!")
        self.log(f'Saved file {filename}')