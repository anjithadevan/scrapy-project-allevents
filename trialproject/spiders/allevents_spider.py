#encoding: utf-8

import scrapy
from scrapy import Request
from scrapy.utils.markup import remove_tags
import dateparser


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
        next_page = response.css(".pagination a::attr(href)").extract()[-1]
        yield scrapy.Request(next_page, callback=self.parse, headers=headers)

    def parse_detail_page(self, response):
        event_time = response.css('.meta-list li:nth-child(1) ::text').extract()[1].strip()
        times = event_time.split('to')
        if len(times)>=2:
            event_time = {'start': dateparser.parse(times[0]),'end': dateparser.parse(times[1])}
        else:
            event_time = {'start': dateparser.parse(times[0]),'end':""}
        if response.css(".orginfo"):
            organizer = {
            'name':response.css('.orginfo .name ::text').extract()[1].strip(), 
            'url':response.css('.orginfo .thumb ::attr(href)').extract_first(),
            'image':response.css('.orginfo .thumb img::attr(src)').extract_first(),
            'followers_count':response.css('.orginfo .detail span::text').extract()[0].split()[0],
            'events_count': response.css('.orginfo .detail span::text').extract()[1].split()[0]
            }
        else:
            organizer = {}
        geo_details = {'latitude': response.css('meta[property="schema:latitude"] ::attr(content)').extract_first(), 'longitude': response.css('meta[property="schema:longitude"] ::attr(content)').extract_first()}
        description = remove_tags(response.css('div[property="schema:description"]').extract_first())
        description=description.replace('\r\n', "")
        yield {
        'event_name': response.css('.overlay-h1 ::text').extract_first(),
        'event_date_time': event_time,
        'address': response.css('.venue-li ::text').extract()[1].strip(),
        'images': response.css('.event-head img::attr(src)').extract(),
        'tickets': {}, 
        'organizer':organizer,
        'description':description,
        'geo_details': geo_details,
        'url': response.url
        }