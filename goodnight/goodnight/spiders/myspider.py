import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://goodnight.at/events']

    custom_settings = {
        'FEEDS': {
            'oGoodnight.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        g=response.xpath('//*[@id="top-inner"]')
        events = g.css('div.event-items-col')
        current_event_index = 0
        stopping_index=1
        for x in events:
            # Extract the time for each event
            time = ''.join(x.css('div.date::text').get()).strip()
            j=response.xpath('//*[@id="main"]')
            event = j.css('div.event-items-col')
            event = event[current_event_index:stopping_index]
            for y in event:  # This line should be indented
                # Select all 'div.event-item-box' elements on the page
                event_boxes = y.css('div.event-item-box')

                for box in event_boxes:

                    # Extract the date and remove extra spaces
                    date = ' '.join(box.css('div.date::text').getall()).strip()

                    title = ' '.join(box.css('div.title-small::text').getall()).strip()
                    if not title:
                        title = ' '.join(box.css('a.link_new::text').getall()).strip()

                    link = box.css('a.link_new::attr(href)').getall()

                    # Single space between each field value
                    date = ' '.join(date.split())
                    title = ' '.join(title.split())
                    time = ' '.join(time.split())
                    date2 = date + ' ' +time

                    yield {
                        'Link': link if link else "This doesn't have a link",
                        'Title': title,
                        'Date': date2,
                    }

            current_event_index += 1
            stopping_index += 1

