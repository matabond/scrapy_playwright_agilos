# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RogJomaItem(scrapy.Item):
    # define the fields for your item here like:
    Source = scrapy.Field()
    cijenaHRK = scrapy.Field()
    cijenaEUR = scrapy.Field()
    url = scrapy.Field()
    opis = scrapy.Field()
    kategorija = scrapy.Field()
    slika = scrapy.Field()
    ime_artikla = scrapy.Field()