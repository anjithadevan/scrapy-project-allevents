import scrapy
from scrapy import Request

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


class EventSpider(scrapy.Spider):
    name = 'eventspider'
    start_urls = ['http://allevents.in/new delhi/all']


    def start_requests(self):
        reqs = []
        for item in self.start_urls:
          reqs.append(Request(url=item, headers=headers))
        return reqs

    def parse(self, response):
        for event in response.css('.event-body'):
            detail_url = event.css('.event-body > .left ::attr(href)').extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_detail_page, headers=headers)

    def parse_detail_page(self, response):
        yield{
        'name': response.css('.overlay-h1 ::text').extract_first(),
        'venu': response.css('.venue-li ::text').extract()[1],
        }