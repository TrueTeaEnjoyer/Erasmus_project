import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.goabase.net/party/?saAtt%5Bcountry%5D=Austria&saAtt%5Bgeoloc%5D=Wien&saAtt%5Bradius%5D=100&saAtt%5Bgeolat%5D=48.2&saAtt%5Bgeolon%5D=16.3&nPos=20']

    custom_settings = {
        'FEEDS': {
            'oGoabase.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Scraping the main page
        self.logger.info(f"Scraping main page: {response}")

        # Extracting links to individual party pages
        links = response.css('a.party-link::attr(href)').getall()

        # Following each link to the party page
        for link in links:
            yield response.follow(link, callback=self.parse_party)

    def parse_party(self, response):
        # Extracting the title from the party page
        title = response.css('span.block.strong.over-hidden::text').get()
        date_time = response.xpath('//*[@id="inner-content"]/div[1]/div[1]/div[1]/div[2]/a[1]/text()').get()
        # Yielding the result with 'Link', 'Title', and 'Date'   fx-grw1 m-b2 m-l10 fs108
        yield {
            'Link': response.url,
            'Title': title,
            'Date': date_time,
        }
