import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.daswerk.org/']

    custom_settings = {
        'FEEDS': {
            'oDaswerk.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Scraping the main page
        self.logger.info(f"Scraping main page: {response}")

        # Extracting links to individual party pages
        links = response.css('a.preview-item--link::attr(href)').getall()

        # Following each link to the party page
        for link in links:
            yield response.follow(link, callback=self.parse_event)

    def parse_event(self, response):
        # Extracting the title from the party page
        title = response.css('p.main--header-title::text').get()
        date = response.css('li::text').get()

        # Yielding the result with 'Link' and 'Title'
        yield {
            'Link': response.url,
            'Title': title,
            'Date': date,
        }
