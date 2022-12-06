# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

# class DuplicatesPipeline:

#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter['id'] in self.ids_seen:
#             raise DropItem(f"Duplicate item found: {item!r}")
#         else:
#             self.ids_seen.add(adapter['id'])
#             return item

class MongoPipeline:

    collection_name = 'rog_joma3'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'rog_joma3')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Start with a clean database
        self.db[self.collection_name].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item