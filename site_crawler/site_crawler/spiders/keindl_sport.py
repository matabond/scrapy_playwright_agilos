import scrapy
from ..items import KeindlSportItem
from ..utils import strip_null, strip_znakovi2, akcija, check_null, prazno
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import logging
import sys
import datetime
import re
#import tracemalloc

logging.basicConfig(handlers=[logging.FileHandler(filename="./log_bike2.txt",encoding='utf-8', mode='w+')],
                    format=u"%(asctime)s::%(threadName)-10s::%(levelname)s::%(name)s::%(lineno)d::%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)

#tracemalloc.start()

class BikeSpider2(scrapy.Spider):
    name = 'keindl_sport'

    def start_requests(self):
        url = "https://keindl-sport.hr/"
        
        yield scrapy.Request(url, callback=self.parse_first, meta=dict(
                playwright = True,
                playwright_include_page = True, 
 
        errback=self.errback,
            ))

    async def parse_first(self, response):
        page=response.meta["playwright_page"] 
        await page.close()
      #  sel = Selector(text=source)
     #   await page.close()

        url2_list=["https://keindl-sport.hr/proizvodi/prodaja-bicikli-bicikli-web-shop/?to_page=20", "https://keindl-sport.hr/proizvodi/e-bicikli/?to_page=7","https://keindl-sport.hr/proizvodi/trenazeri/" "https://keindl-sport.hr/proizvodi/dijelovi-bicikli-prodaja-web/?to_page=61", "https://keindl-sport.hr/proizvodi/oprema/?to_page=37", ]  
        for url2 in url2_list:
            yield(scrapy.Request(url2, callback=self.parse_site, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                    playwright_page_methods = [
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                #  PageMethod("wait_for_selector", 'div.load-more-container.c-load-more-container a.btn.btn-load-more-catalog.load-more.btn-load-more'),
                #  PageMethod("click", 'div.load-more-container.c-load-more-container a.btn.btn-load-more-catalog.load-more.btn-load-more')
                #  PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")

                    ],

        errback=self.errback,
            )))


    async def parse_site(self, response):
        page = response.meta["playwright_page"]
        source = await page.content()
        print(f"url1: {response.url}")
        sel = Selector(text=source)
        await page.close()
        extracted_links_site=set()
        for link in sel.css('div.cp-price'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links_site.add(link.css('a::attr(href)').get())
            


        #url_prod="https://keindl-sport.hr/cube-flying-circus-240-galacticnblack-2023-proizvod-51415/"   

        for url_prod in extracted_links_site:
            print("link2:", url_prod)

            yield(scrapy.Request(url_prod, callback=self.parse_item, meta=dict(
                        playwright = True,
                        playwright_include_page = True,
                        # playwright_page_methods =[
                        #     PageMethod('wait_for_selector', 'div.content-page'),
                        # ],
                errback=self.errback,
                    )))


    async def parse_item(self, response):
            page = response.meta["playwright_page"]
            source = await page.content()
            print(f"url yieldan: {response.url}")
            sel = Selector(text=source) 
            await page.close()       
            
        # dodajem dolje definiranu funkciju strip_null koja zapravo provjerava je li element null i ako nije koristi funkciju strip kako bi se riješio nepotrebnih bjelina 
            bike_item = KeindlSportItem() 
            bike_item['price_before'] = None
            bike_item['price_eur'] = coalesce(strip_znakovi2(strip_null(sel.css('div.cd-price div.cd-current-price.red span[data-product_price]::text').extract_first())), strip_znakovi2(strip_null(sel.css('div.cd-price div.cd-current-price[data-product_price] span::text').extract_first())))
            bike_item['brend'] = strip_null(sel.css('div.cd-brand img::attr(alt)').extract_first())
            bike_item['title'] = strip_null(sel.css('div.cd-title-cnt h1[data-product_title]::text').extract_first())
            bike_item['discount'] = None
            # src=strip_null(response.css('div.p_info_image_wrapper img::attr(src)').extract_first())
            # if src is not None:                 
            bike_item['src'] = None
            bike_item['description'] = None
            bike_item['link'] = response.url
            bike_item['ppn_dtm']=datetime.datetime.now()
            bike_item['breadcrumb'] = sel.css('div.bc-cnt div.bc > a[href]::text').extract()
            bike_item['coupons']=None
            yield bike_item


    
    async def errback(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()




def coalesce(*values):
    """Return the first non-None value or None if all values are None"""
    return next((v for v in values if v is not None), None)

# print(f"memorija:{tracemalloc.get_traced_memory()}")

# # stopping the library
# tracemalloc.stop()

log = open("myprog.log", "w+")
sys.stdout = log