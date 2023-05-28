import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

from hw_9_scrapy.my_spyder.my_spyder.pipelines import MySpyderPipeline


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # custom_settings = {"ITEM_PIPLINES" : {MySpyderPipelineQuotes:300}}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {'ITEM_PIPELINES': {MySpyderPipeline: 100}}  # {"FEED_FORMAT": "json", "FEED_URI": "result.json"}
    START_INDEX = 0
    def parse(self, response, *args):
        for el in response.xpath("/html//div[@class='quote']"):
            tags = [e.strip() for e in el.xpath("div[@class='tags']/a[@class='tag']/text()").extract()]
            author = el.xpath("span/small[@class='author']/text()").get().strip()
            quote = el.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(
                url=self.start_urls[self.START_INDEX] + el.xpath("span/a/@href").get().strip(),
                # callback=self.parse_author
            )
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(url=self.start_urls[self.START_INDEX] + next_link.strip())
            # yield response.follow(new_link, callback=self.parse)
            # yield scrapy.Request(url=self.start_urls[0] + new_link)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    print('Process finished!')