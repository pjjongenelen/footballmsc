import scrapy


class QuotesSpider(scrapy.Spider):
    name = "fotmob"

    def start_requests(self):
        urls = [
            'https://www.fotmob.com/match/3602655/matchfacts/fc-twente-vs-psv-eindhoven'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'{page}.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {filename}')
