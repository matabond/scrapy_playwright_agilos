import json
import re
from urllib.parse import urljoin
import scrapy
from scrapy_playwright.page import PageMethod 
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..items import RogJomaItem
import validators
from ..utils import regexp
import datetime

class Rog_Joma_Spider(scrapy.Spider):
    name = 'rog_joma'
    start_urls = ['https://www.rog-joma.hr/']
    allowed_domains = ['rog-joma.hr']
    # urls = set()
    def start_requests(self):
        url = "https://www.rog-joma.hr/"
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
        extracted_urls = set()
        for link in sel.xpath("//a/@href").getall():
            link = response.urljoin(link)
            if validators.url(link):
                extracted_urls.add(link)
        await page.close()

        for url in extracted_urls:
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
            sel = Selector(text=response.body)
            items=sel.xpath("//div[@class='product_cnt_border']").getall()
            for i in items:
                sel2=Selector(text=i)
                cijenaHRK = sel2.xpath("//span[@class='product_price_amount']/text()").get().replace(' ','') #cijena u sebi ima blankove
                cijenaEUR = sel2.xpath("//div[@class='productPriceEurTrans']/text()").get().replace(' ','') #cijena u sebi ima blankove
                url = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/@href").get()
                ime_artikla = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_name']/text()").get()
                kategorija = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_brand']/text()").get()
                slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@data-src").get()
                if slika is None:
                    slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@src").get()

                item=RogJomaItem()
                item['source_link']=response.url
                item['cijena_hrk']=regexp(r"\d+\,\d*",cijenaHRK).replace(',','.')
                item['cijena_eur']=regexp(r"\d+\,\d*",cijenaEUR).replace(',','.')
                item['item_url']='https://www.rog-joma.hr'+url
                item['ime_artikla']=ime_artikla
                item['kategorija']=kategorija
                item['slika_url']=slika
                item['ppn_dtm']=datetime.datetime.now()
                page = response.meta.get("playwright_page")
                await page.close()
                yield item
        except:
            self.con.print_exception()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()