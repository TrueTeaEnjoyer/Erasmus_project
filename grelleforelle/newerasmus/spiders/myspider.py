import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.grelleforelle.com/programm/']

    custom_settings = {
        'FEEDS': {
            'oGrelleforelle.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # We selects all unique links on the page that start with the specified address
        links = set(response.css('a[href^="https://www.grelleforelle.com/project/"]::attr(href)').extract())
        for link in links:
            
            # We extracts all text within <a> tags, removes extra whitespace, and cleans up duplicates
            date_performer = [text.strip() for text in response.xpath(f'//a[@href="{link}"]/text()').getall() if text.strip()]
            date_performer = list(dict.fromkeys(date_performer))

            yield {
                'Link': link,
                'Date(s)/Performer(s)': date_performer,
            }
