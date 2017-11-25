import scrapy
from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


class EventSpider(scrapy.Spider):
    name = 'eventspiderall'
    start_urls = ['http://allevents.in/new delhi/all']
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination elist-pager',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        for event in response.css('.event-body'):
            yield {'name': event.css('a ::text').extract_first()}
        item_links = response.css('.event-body > .left ::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)    
            
    def start_requests(self):
        reqs = []
        for item in self.start_urls:
          reqs.append(Request(url=item, headers=headers))
        return reqs
    def parse_detail_page(self, response):
        yield{}