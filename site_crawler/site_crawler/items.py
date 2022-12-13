# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RogJomaItem(scrapy.Item):
    # define the fields for your item here like:
    source_link = scrapy.Field()
    cijena_hrk = scrapy.Field()
    cijena_eur = scrapy.Field()
    item_url = scrapy.Field()
    # opis = scrapy.Field()
    kategorija = scrapy.Field()
    slika_url = scrapy.Field()
    ime_artikla = scrapy.Field()


class BikeDiscountItem(scrapy.Item):
    # define the fields for your item here like:
    source_link = scrapy.Field()
    cijena_popust = scrapy.Field()
    cijena = scrapy.Field()
    item_url = scrapy.Field()
    # opis = scrapy.Field()
    kategorija = scrapy.Field()
    slika_url = scrapy.Field()
    ime_artikla = scrapy.Field()