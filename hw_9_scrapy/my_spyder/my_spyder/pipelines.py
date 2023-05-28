# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class MySpyderPipelineQuotes(object):
    quotes_list = []
    authors_list = []

    def process_item(self, item, spider):

        adapted_item = ItemAdapter(item)
        # print(adapted_item)
        if "author" in adapted_item.keys():
            self.quotes_list.append(item)
        elif 'fullname' in adapted_item.keys():
            self.authors_list.append(item)

        return item

    def close_spyder(self, spyder):

        with open("authors.json", "w") as file:
            json.dump(self.authors_list, file, indent=4)

        with open("quotes.json", "w") as file:
            json.dump(self.quotes_list, file, indent=4)
