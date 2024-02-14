import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://flex.at/']

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'oFlex.json': {
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
        titles = response.css('h2.ectbe-evt-title.elementor-repeater-item-f75b093::text').getall()
        days = response.css('span.ectbe-ev-day::text').getall()
        months = response.css('span.ectbe-ev-mo::text').getall()
        times = response.css('div.ectbe-evt-time.elementor-repeater-item-fd61cbc::text').getall()
        links = response.css('a.ectbe-evt-read-more::attr(href)').getall()
        # Iterate over the data and yield JSON objects
        for title, day, month, time, link in zip(titles, days, months, times, links):
            yield {
                'Link': link.strip(),
                'Title': title.strip(),
                'Date': day.strip() + ' ' + month.strip() + ' ' + time.strip(),

            }
