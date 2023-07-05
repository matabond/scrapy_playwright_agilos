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
import logging

logging.basicConfig(handlers=[logging.FileHandler(filename="./log_bike2.txt",encoding='utf-8', mode='w+')],
                    format=u"%(asctime)s::%(threadName)-10s::%(levelname)s::%(name)s::%(lineno)d::%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)



class BikeSpider(scrapy.Spider):
    name = 'bike_discount_part6'
    allowed_domains = ['bike-discount.de']

    """
    playwright_include_page If True, the Playwright page that was used to download the request will be available in the callback via response.meta['playwright_page'].
    """
    def start_requests(self):

        url = "https://www.bike-discount.de/en/cycling-clothing?p=101"   #polovicu scrape-at

        yield(scrapy.Request(url, callback=self.parse_site, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                    # playwright_page_methods =[
                    #     PageMethod('wait_for_selector', 'div.product--info'),
                    # ],
            errback=self.errback,
                )))


    async def parse_site(self, response):

        print('trenutna stranica: ', response.url)
        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()

        extracted_links_site=set()

        for link in sel.css('div.product--info'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links_site.add(link.css('a::attr(href)').get())
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
                # playwright_page_methods =[
                #     PageMethod('wait_for_selector', 'div.product--info'),
                # ]))     
            errback=self.errback,
                ))

        for idx, url in enumerate(extracted_links_site):
            if validators.url(url):
                print(f"url2: {url}")
                yield(scrapy.Request(url, callback=self.parse_item, meta=dict(
                    playwright = True,
                    playwright_include_page = True,
            errback=self.errback
                )))

    async def parse_item(self, response):

        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        bike_item = BikeDiscountItem() 
        bike_item['price_before'] = strip_znakovi(strip_null(sel.css('span.price--line-through span::text').extract_first()))
        bike_item['price_eur'] = strip_znakovi(strip_null(sel.css('span.price--content.content--default span::text').extract_first()))
        bike_item['brend'] = strip_null(sel.css('div.product--headername h1.product--title strong::text').extract_first())
        bike_item['discount'] =akcija(strip_null(sel.css('span.price--discount-percentage::text').extract_first()))
        bike_item['src'] = strip_null(sel.css('img::attr(src)').extract_first())
        bike_item['description'] = strip_null(sel.css('div.product--description ::text').extract_first() ) #kako ovo popraviti -umjesto get() stavila extract_first().strip()
        bike_item['link'] = response.url
        bike_item['breadcrumb'] = sel.css('nav.content--breadcrumb.block ul.breadcrumb--list > li.breadcrumb--entry a::attr(title)').extract()
        print(f"yielded link: {bike_item['link']}")
        bike_item['ppn_dtm']=datetime.datetime.now()
        bike_item['coupons']=None
        try:
            bike_item['title'] = strip_null(sel.css('div.product--headername ::text').extract()[3])

        except IndexError:
            bike_item['title'] = None
#           bike_item['specif'] = bike.css('div.product--properties.panel.has--border *::text').extract_first()  #kako dohvatiti sav tekst? Izgleda da mi to ipak ne treba
        # gc.collect()
        yield bike_item


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    
log = open("myprog.log", "w+")
sys.stdout = log