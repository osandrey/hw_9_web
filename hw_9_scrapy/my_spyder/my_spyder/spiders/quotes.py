import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # custom_settings = {"ITEM_PIPLINES" : {MySpyderPipelineQuotes:300}}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]


    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract_first(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        new_link = response.xpath("//li[@class='next']/a/@href").get()
        if new_link:
            yield response.follow(new_link, callback=self.parse)
            # yield scrapy.Request(url=self.start_urls[0] + new_link)


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()