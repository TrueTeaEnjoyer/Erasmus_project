import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.goabase.net/party/?saAtt[geoloc]=wien&saAtt[radius]=100&saAtt[geolat]=48.2&saAtt[geolon]=16.3']

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
        title = response.css('h2::text').get()
        date = response.xpath('//*[@id="inner-content"]/div[1]/div[1]/div[1]/div[2]/a[1]/text()').get()

        # Yielding the result with 'Link' and 'Title' and 'Date'
        yield {
            'Link': response.url,
            'Title': title,
            'Date': date,
        }
