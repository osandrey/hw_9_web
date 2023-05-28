import scrapy
import collections
import sys

from ..pipelines import *


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"ITEM_PIPLINES": {MySpyderPipelineQuotes: 100}}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='author-details']"):
            yield {

                "fullname" : quote.xpath("h3[@class='author-title']/text()").get().strip(),
                "date_born" : quote.xpath("p/span[@class='author-born-date']/text()").get().strip(),
                "born_location" : quote.xpath("p/span[@class='author-born-location']/text()").get().strip(),
                "description" : quote.xpath("div[@class='author-description']/text()").get().strip()
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
