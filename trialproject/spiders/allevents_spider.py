import scrapy
from scrapy import Request

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


class EventSpider(scrapy.Spider):
    name = 'eventspider'
    start_urls = ['http://allevents.in/new delhi/all']

    def parse(self, response):
        for event in response.css('.event-body'):
            yield {'name': event.css('a ::text').extract_first()}

    def start_requests(self):
        reqs = []
        for item in self.start_urls:
          reqs.append(Request(url=item, headers=headers))
        return reqs