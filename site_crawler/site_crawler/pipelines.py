# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
import psycopg

from scrapy.exceptions import DropItem
import datetime

class PostgresPipeline:

    # def __init__(self, postgres_uri, postgres_db):
    #     self.postgres_uri = postgres_uri
    #     self.postgres_db = postgres_db

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         postgres_uri=crawler.settings.get('POSTGRES_URI'),
    #         postgres_db=crawler.settings.get('POSTGRES_DATABASE')
    #     )

    def open_spider(self, spider):
        self.connection = psycopg.connect("dbname=scraping user=postgres password=mysecretpassword host=localhost port=5432")
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO public.rog_joma(ppn_dtm,source_link, cijena_hrk, cijena_eur, url,  kategorija, slika_url, ime_artikla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (item['ppn_dtm'],item['source_link'],item['cijena_hrk'],item['cijena_eur'],item['item_url'],item['kategorija'],item['slika_url'],item['ime_artikla']))
        self.connection.commit()
        return item

class MongoPipeline:
    collection_name = 'rog_joma'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'rog_joma')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Start with a clean database
        # self.db[self.collection_name].delete_many({})
        # self.time = datetime.datetime.now()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item