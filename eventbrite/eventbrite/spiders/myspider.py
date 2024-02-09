import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.eventbrite.at/o/black-market-33429549183']

    custom_settings = {
        'FEEDS': {
            'oEventbrite.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Keep track of seen title-link-date triples
        seen_triples = set()

        # Extract information from each event card
        event_cards = response.css('div.eds-event-card--consumer')

        for card in event_cards:
            link = card.css('a.eds-event-card-content__action-link::attr(href)').get()
            title = card.css('div.eds-event-card__formatted-name--is-clamped::text').get()
            date = card.css('div.eds-event-card-content__sub-title.eds-text-color--primary-brand.eds-l-pad-bot-1.eds-l-pad-top-2.eds-text-weight--heavy.eds-text-bm::text').get()

            # Check if the title-link-date triple is not seen before
            if title and link and date and (title, link, date) not in seen_triples:
                seen_triples.add((title, link, date))

                yield {
                    'Link': link,
                    'Title': title,
                    'Date': date,
                }

        # Follow pagination links if available
        next_page = response.css('a.pagination__next-link::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
