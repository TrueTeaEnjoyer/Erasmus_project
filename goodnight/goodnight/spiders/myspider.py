import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://goodnight.at/events', 'https://goodnight.at/events?view=events&start_offset=1']

    custom_settings = {
        'FEEDS': {
            'oGoodnight.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Select all 'div.event-item-box' elements on the page
        event_boxes = response.css('div.event-item-box')

        for box in event_boxes:
            # Extract the date and remove extra spaces
            date = ' '.join(box.css('div.date::text').getall()).strip()

            # Check if the date falls among values to be skipped, if so, skip to the next record
            if date in ["4.12.23", "5.12.23", "6.12.23", "7.12.23", "8.12.23", "9.12.23", "10.12.23", "11.12.23", "12.12.23", "13.12.23"]:
                continue

            # Extract the title ('div.title-small'), if not present, consider the text from 'a.link_new'
            title = ' '.join(box.css('div.title-small::text').getall()).strip()
            if not title:
                title = ' '.join(box.css('a.link_new::text').getall()).strip()

            # Extract the link ('a.link_new' href attribute)
            link = box.css('a.link_new::attr(href)').get()

            # Single space between each field value
            date = ' '.join(date.split())
            title = ' '.join(title.split())

            # Return the cleaned data in a JSON record
            yield {
                'Link': link if link else "This doesn't has link",
                'Title': title,
                'Date': date,

            }
