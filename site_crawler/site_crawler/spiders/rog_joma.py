import json
import re
from urllib.parse import urljoin
import scrapy
from scrapy_playwright.page import PageMethod 
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..items import RogJomaItem
import validators
from ..utils import regexp, izvuci_cijenu
import datetime

import logging
logging.basicConfig(handlers=[logging.FileHandler(filename="./log.txt",encoding='utf-8', mode='a+')],
                    format=u"%(asctime)s::%(threadName)-10s::%(levelname)s::%(name)s::%(lineno)d::%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)

class Rog_Joma_Spider(scrapy.Spider):
    name = 'rog_joma'
    start_urls = ['https://www.rog-joma.hr/']
    allowed_domains = ['rog-joma.hr']
    # urls = set()
    def start_requests(self):
        url = "https://www.rog-joma.hr/"
        logging.info(f"1url: {url}")
        yield scrapy.Request(
            url,callback=self.parse,
            meta = {
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # PageMethod("wait_for_selector", "//a/@href"),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
                ],
                "errback": self.errback,
            }
        )

    async def parse(self, response):
        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)
        await page.close()
        extracted_urls = set()
        for link in sel.xpath("//a/@href").getall():
            link = response.urljoin(link)
            if validators.url(link):
                extracted_urls.add(link)

        for url in extracted_urls:
            logging.info(f"2url: {url}")
            yield scrapy.Request(
            url,callback=self.parse_site,
            meta={"playwright":True,"playwright_include_page":True,"playwright_page_methods":[
                PageMethod("wait_for_selector","//div[@class='product_list_cnt productList']"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
            ]},
            errback=self.errback,
            )

    async def parse_site(self,response):
        try:
            page = response.meta.get("playwright_page")
            source = await page.content()
            sel = Selector(text=source)
            await page.close()
            items=sel.xpath("//div[@class='product_cnt_border']").getall()
            for i in items:
                sel2=Selector(text=i)
                # cijena_prije_akcije = sel2.xpath("//span[@class='product_price_pmc_label']/text()").get().replace(' ','')
                # cijenaEUR = sel2.xpath("//div[@class='product_price_amount']/text()").get().replace(' ','') #cijena u sebi ima blankove
                url = 'https://www.rog-joma.hr'+sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/@href").get()
                # ime_artikla = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_name']/text()").get()
                # kategorija = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_brand']/text()").get()
                # slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@data-src").get()
                # if slika is None:
                #     slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@src").get()

                if validators.url(url):
                    logging.info(f"3url: {url}")
                    yield scrapy.Request(
                    url,callback=self.parse_item,
                    meta={"playwright":True,"playwright_include_page":True,"playwright_page_methods":[
                        PageMethod("wait_for_selector","//span[@class='productSalePriceAmount']"),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
                    ]},
                    errback=self.errback,
                    )
        except:
            self.con.print_exception()

    async def parse_item(self,response):

        page = response.meta.get("playwright_page")
        source = await page.content()
        sel = Selector(text=source)


        opis=sel.xpath("//div[@class='descriptionTabsSection']//text()").getall()
        full_opis=""
        for o in opis:
            if isinstance(o, str):
                full_opis=full_opis+o.strip()+'\n'

        ime_artikla=sel.xpath("//h1[@class='product_title']/text()").get()
        source_link=sel.xpath("//div[@class='product_brand_logo']/a/@href").get()
        kategorija=sel.xpath("//div[@class='product_brand_logo']/a/@title").get()
        cijena_prije_akcije = sel.xpath("//span[@class='productReducedPriceAmount']/text()").get()
        cijenaEUR = sel.xpath("//span[@class='productSalePriceAmount']/text()").get()
        item=RogJomaItem()
        item['link']=response.url
        item['price_before']=izvuci_cijenu(cijena_prije_akcije)
        item['price_eur']=izvuci_cijenu(cijenaEUR) #ako ne skupljam onda stavljam 0.0
        item['title']=ime_artikla
        item['brend']=kategorija
        item['source_link']=source_link
        item['description']=full_opis.strip()
        item['discount']=True if item['price_before'] > 0.0 else False
        item['ppn_dtm']=datetime.datetime.now()
        item['src'] = sel.css('div.col-12.col-lg-7.product_detail_picture_column div.bicycleDetailZoomCnt a::attr(href)').extract_first()
        item['breadcrumb'] = sel.css('div.col-12.breadcrumbs_cnt.bottom ul.breadcrumb_list > li a:not(:last-child)::attr(title)').extract()
        item['coupons']=None

        await page.close()
        yield item


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()