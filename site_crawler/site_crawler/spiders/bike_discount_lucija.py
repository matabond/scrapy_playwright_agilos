import scrapy
from ..items import BikeDiscountItem
from scrapy_playwright.page import PageMethod
import logging
from scrapy.selector import Selector
import validators

class BikeSpider2(scrapy.Spider):
    name = 'bike_discount_lucija'

    def start_requests(self):
        url = "https://www.bike-discount.de/en/"        
        yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[
                    PageMethod('wait_for_selector', 'div.sub-navigation'),
                ],
        errback=self.errback,
            ))

    async def parse(self, response):
        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        extracted_links=set()
        for link in sel.css('div.sub-navigation li.navigation--entry'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links.add(link.css('a::attr(href)').get())
        print('linkovi:', extracted_links)

        for idx, url in enumerate(extracted_links):
            if validators.url(url):
                yield(scrapy.Request(url, callback=self.parse_site, meta=dict(
                    playwright = True,
                    playwright_context = "context-"+str(idx),
                    playwright_include_page = True, 
                    playwright_page_methods =[
                        PageMethod('wait_for_selector', 'div.product--info'),
                    ],
            errback=self.errback,
                )))

    async def parse_site(self, response):
        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        #await page.context.close()
        extracted_links_site=set()
       # extracted_links_site=set()
        for link in sel.css('div.product--info'):    # dohvati mi sve li.navigation--entry unutar div.sub-nav....
            extracted_links_site.add(link.css('a::attr(href)').get())
        print('linkovi:', extracted_links_site, 'duljina:', len(extracted_links_site))
        next_page = sel.css('div.listing--bottom-paging a[title*=Next]').attrib['href']  #ovo bi sad trebalo bit ok ali za zadnjem ne može uzet next pa je tu greška, to riješi
        if next_page is not None:
            next_page_url = 'https://www.bike-discount.de' + next_page
            print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_site, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[
                    PageMethod('wait_for_selector', 'div.product--info'),
                ]))        

        for idx, url in enumerate(extracted_links_site):
            if validators.url(url):
                yield(scrapy.Request(url, callback=self.parse_item, meta=dict(
                    playwright = True,
                    playwright_include_page = True,
                    playwright_context = "context2-"+str(idx),
                    # playwright_page_methods =[
                    #     PageMethod('wait_for_selector', 'div.content.product--details'),  # micanjem ovoga riješila TimeoutError
                    # ],
            errback=self.errback,
                )))

    async def parse_item(self, response):
            page = response.meta.get("playwright_page")
            source = await page.content()
            sel = Selector(text=source)
            await page.close()
            # page = response.meta["playwright_page"]
            # await page.content()
            # await page.close()      
            #for bike in response.css('div.content.product--details'):
            # dodajem dolje definiranu funkciju strip_null koja zapravo provjerava je li element null i ako nije koristi funkciju strip kako bi se riješio nepotrebnih bjelina 
            bike_item = BikeDiscountItem() 
            bike_item['price_before'] = strip_null(sel.css('span.price--line-through span::text').extract_first())
            bike_item['price_eur'] = strip_null(sel.css('span.price--content.content--default span::text').extract_first())
            bike_item['brend'] = strip_null(sel.css('div.product--headername h1.product--title strong::text').extract_first())
            bike_item['title'] = strip_null(sel.css('div.product--headername ::text').extract()[3])
            bike_item['discount'] =strip_null(sel.css('span.price--discount-percentage::text').extract_first())
            bike_item['src'] = strip_null(sel.css('img::attr(src)').extract_first())
            bike_item['description'] = strip_null(sel.css('div.product--description ::text').extract_first() ) #kako ovo popraviti -umjesto get() stavila extract_first().strip()
            bike_item['link'] = response.url
    #           bike_item['specif'] = bike.css('div.product--properties.panel.has--border *::text').extract_first()  #kako dohvatiti sav tekst? Izgleda da mi to ipak ne treba
            yield bike_item

    async def errback(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()

def strip_null(x):

    if x is not None:
        x=x.strip()
    return x