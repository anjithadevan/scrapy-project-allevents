import scrapy


class MySpider(scrapy.Spider):
    name = "events"
    start_urls = [
        'https://allevents.in/new%20delhi/all',
    ]
    def parse(self, response):
        for event in response.css('div'):
            yield {
                'name': event.css('h3 a::text').extract_first(),
            }