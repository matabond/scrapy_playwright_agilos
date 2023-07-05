import scrapy
from ..items import BikeDiscountItem
from ..utils import strip_null, strip_znakovi, akcija
from scrapy_playwright.page import PageMethod
import logging
from scrapy.selector import Selector
import validators
import re
import datetime
import sys
import tracemalloc
import time


# import gc
# from scrapy_playwright import PlaywrightRequest

# from scrapy.http import HtmlResponse
# from scrapy_playwright.driver import PlaywrightDriver
# from scrapy_playwright.driver import PlaywrightBrowser


import logging
logging.basicConfig(handlers=[logging.FileHandler(filename="./log_bike2.txt",encoding='utf-8', mode='w+')],
                    format=u"%(asctime)s::%(threadName)-10s::%(levelname)s::%(name)s::%(lineno)d::%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


class BikeSpider(scrapy.Spider):
    name = 'bike_discount_browser'
    allowed_domains = ['bike-discount.de']
    tracemalloc.start()

    """
    playwright_include_page If True, the Playwright page that was used to download the request will be available in the callback via response.meta['playwright_page'].
    """
    def start_requests(self):
        start_time = time.time()
        url = "https://www.bike-discount.de/en/"

        yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[
                    PageMethod('wait_for_selector', 'div.sub-navigation'),
                ],
        errback=self.errback,
            ))
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Task1 completed in {elapsed_time:.2f} seconds.')

    async def parse(self, response):
        start_time = time.time()
        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        # gc.collect()
        extracted_links=set()
        for link in sel.css('div.sub-navigation li.navigation--entry'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links.add(link.css('a::attr(href)').get())
        print(f"linkovi: {extracted_links}")

        for idx, url in enumerate(extracted_links):
            if validators.url(url):
                yield(scrapy.Request(url, callback=self.parse_site, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                    playwright_page_methods =[
                        PageMethod('wait_for_selector', 'div.product--info'),
                    ],
            errback=self.errback,
                )))
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Task2 completed in {elapsed_time:.2f} seconds.')

    async def parse_site(self, response):
        start_time = time.time()
        page = response.meta.get("playwright_page")
        print(f"url1: {response.url}")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        # gc.collect()
        extracted_links_site=set()

        for link in sel.css('div.product--info'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links_site.add(link.css('a::attr(href)').get())
#        next_page = sel.css('div.listing--bottom-paging a[title*=Next]').attrib['href']  #ovo bi sad trebalo bit ok ali za zadnjem ne moze uzet next pa je tu greska, to rijesi
        try: 
            next_page = sel.css('div.listing--bottom-paging a[title*=Next]').attrib['href']
            next_page_url = 'https://www.bike-discount.de' + next_page
        except KeyError:
            next_page_url=None
        if next_page_url is not None:
#        if next_page:   #maknula "is not None"
#            next_page_url = 'https://www.bike-discount.de' + next_page
            print(f"next_page_url: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse_site, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[
                    PageMethod('wait_for_selector', 'div.product--info'),
                ]))        

        for idx, url in enumerate(extracted_links_site):
            if validators.url(url):
                print(f"url_potreban: {url}")
                yield(scrapy.Request(url, callback=self.parse_item, meta=dict(
                    playwright = True,
                    playwright_include_page = True,
            errback=self.errback
                )))
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Task3 completed in {elapsed_time:.2f} seconds.')

    async def parse_item(self, response):
        start_time = time.time()
        page = response.meta.get("playwright_page")
        print(f"url yieldan: {response.url}")
        # page.wait_for_timeout(100000)
        source = await page.content()
        sel = Selector(text=source)
        # await page.context.close()
        await page.close()
        #for bike in response.css('div.content.product--details'):
        # dodajem dolje definiranu funkciju strip_null koja zapravo provjerava je li element null i ako nije koristi funkciju strip kako bi se rijesio nepotrebnih bjelina 
        bike_item = BikeDiscountItem() 
        bike_item['price_before'] = strip_znakovi(strip_null(sel.css('span.price--line-through span::text').extract_first()))
        bike_item['price_eur'] = strip_znakovi(strip_null(sel.css('span.price--content.content--default span::text').extract_first()))
        bike_item['brend'] = strip_null(sel.css('div.product--headername h1.product--title strong::text').extract_first())
        bike_item['discount'] =akcija(strip_null(sel.css('span.price--discount-percentage::text').extract_first()))
        bike_item['src'] = strip_null(sel.css('img::attr(src)').extract_first())
        bike_item['description'] = strip_null(sel.css('div.product--description ::text').extract_first() ) #kako ovo popraviti -umjesto get() stavila extract_first().strip()
        bike_item['link'] = response.url
        bike_item['ppn_dtm']=datetime.datetime.now()
        try:
            bike_item['title'] = strip_null(sel.css('div.product--headername ::text').extract()[3])

        except IndexError:
            bike_item['title'] = None
#           bike_item['specif'] = bike.css('div.product--properties.panel.has--border *::text').extract_first()  #kako dohvatiti sav tekst? Izgleda da mi to ipak ne treba
        # gc.collect()
        yield bike_item
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Task4 completed in {elapsed_time:.2f} seconds.')

    async def errback(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()

    print(f"memorija:{tracemalloc.get_traced_memory()}")

    # stopping the library
    tracemalloc.stop()




log = open("myprog.log", "w+")
sys.stdout = log

