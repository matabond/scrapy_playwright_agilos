import scrapy
from ..items import ExtremeVitalItem
from ..utils import strip_null, strip_znakovi2, akcija, check_null, prazno, nlp_analiza
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
    name = 'extreme_vital'

    def start_requests(self):
        url = "https://www.extremevital.com/en/"
        yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright = True,
                playwright_include_page = True, 
    
        errback=self.errback,
            ))

    async def parse(self, response):
        page=response.meta["playwright_page"] 
        source = await page.content()
        sel = Selector(text=source)
        await page.close()  
        extracted_links=set()
        for link in sel.css('li#bikes ul.sub_menu.level1 > li.sub'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links.add(link.css('a::attr(href)').extract_first())
        for url2 in extracted_links:
            print(url2)
        #print(len(extracted_links))

       # url2="https://www.extremevital.com/hr/bicikli/bicikli-c-1.html"  # test na:"https://www.bike-discount.de/en/bike-accessories"  došlo do 38. stranice

            yield(scrapy.Request(url2, callback=self.parse_site, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                    # playwright_page_methods =[
                    #     PageMethod('wait_for_selector', 'div.product--info'),
                    # ],
            errback=self.errback,
                )))

    async def parse_site(self, response):
        page = response.meta["playwright_page"]
        source = await page.content()
        print(f"url1: {response.url}")
        sel = Selector(text=source)
        await page.close()  
        extracted_links_site=set()
        for link in sel.css('div.product-block'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links_site.add(link.css('a::attr(href)').get())
        try: 
            next_page = sel.css('div.cpaging span.next a').attrib['href']
            next_page_url = next_page
        except KeyError:
            next_page_url=None
        if next_page_url is not None:
#        if next_page:   #maknula "is not None"
#            next_page_url = 'https://www.bike-discount.de' + next_page
            print(f"next_page_url: {next_page_url}")
        # if next_page is not None:
        #     next_page_url = 'https://www.bike-discount.de' + next_page
            yield (scrapy.Request(next_page_url, callback=self.parse_site, meta=dict(
                playwright = True,
                playwright_include_page = True, 

            errback=self.errback,
                )))       
        for url_prod in extracted_links_site:
             print("link2:", url_prod)

             yield(scrapy.Request(url_prod, callback=self.parse_item, meta=dict(
                playwright = True,
                playwright_include_page = True,
             errback=self.errback,
                )))


    async def parse_item(self, response):
            page = response.meta["playwright_page"]
            source = await page.content()
            print(f"url yieldan: {response.url}")  
            sel = Selector(text=source)   
            await page.close()  
            
        # dodajem dolje definiranu funkciju strip_null koja zapravo provjerava je li element null i ako nije koristi funkciju strip kako bi se riješio nepotrebnih bjelina 
            bike_item = ExtremeVitalItem() 
            bike_item['price_before'] = strip_znakovi2(strip_null(sel.css('div.old_price span.number::text').extract_first()))
            bike_item['price_eur'] = prazno(check_null(strip_znakovi2(strip_null(sel.css('div.new_price span.number::text').extract_first())), strip_znakovi2(strip_null(sel.css('div.final_price span.number::text').extract_first())), strip_znakovi2(strip_null(sel.css('div.reg_price span.number::text').extract_first()))))
            bike_item['brend'] = strip_null(sel.css('h1.products_name div.manufacturer::text').extract_first())
            bike_item['title'] = strip_null(sel.css('h1.products_name div.product::text').extract_first())
            bike_item['discount'] = akcija(strip_null(sel.css('div#p_info_main_image span.discount-dot strong::text').extract_first()))
            src=strip_null(response.css('div.p_info_image_wrapper img::attr(src)').extract_first())
            if src is not None:                 
                bike_item['src'] = "https://www.extremevital.com"+src
            bike_item['description'] = strip_null(sel.css('div#product--description.active div.tab-content p::text').extract_first() ) #kako ovo popraviti -umjesto get() stavila extract_first().strip()
            bike_item['link'] = response.url
            bike_item['ppn_dtm']=datetime.datetime.now()
            bike_item['breadcrumb'] = sel.css('div#crumbs ul.clearfix > li a:not(:last-child) span::text').extract()
            bike_item['coupons'] = nlp_analiza(sel.css('div#eligible_coupons p::text').extract_first())
            yield bike_item

    
    async def errback(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()

    # displaying the memory

# print(f"memorija:{tracemalloc.get_traced_memory()}")

# # stopping the library
# tracemalloc.stop()

log = open("myprog.log", "w+")
sys.stdout = log