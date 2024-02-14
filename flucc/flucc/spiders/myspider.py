import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):
    name = 'myspider'
    start_urls = ['https://www.flucc.at/']

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'oFlucc.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    rules = [
        Rule(LinkExtractor(allow='events'), callback='parse_item')
    ]

    # Method responsible for processing responses
    def parse_item(self, response):
        # Log the visited URL and the status code
        self.log(f"Visited {response.url} with status code {response.status}")

        date = response.css('p.date.uppercase::text').get().strip()
        time = response.css('p.time::text').get().strip()
        event = response.css('h2::text').get().strip()

        yield {
            'Link': response.url,
            'Event': event,
            'Date': date + ' ' + time
        }
