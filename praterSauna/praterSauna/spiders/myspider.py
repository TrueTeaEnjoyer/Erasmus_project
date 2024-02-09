import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://pratersauna.tv/programm/']

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'oPratersauna.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    # Method responsible for processing responses
    def parse(self, response):
        # Log the visited URL and the status code
        self.log(f"Visited {response.url} with status code {response.status}")

        # Extract interesting data using CSS selectors
        titles = response.css('h1.entry-title::text').getall()

        # Iterate over the data and yield JSON objects
        for title in titles:
            yield {
                'Title': title.strip(),
            }

