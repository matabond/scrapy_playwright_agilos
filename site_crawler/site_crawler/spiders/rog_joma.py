import json
import re
from urllib.parse import urljoin
import scrapy
from scrapy_playwright.page import PageMethod 
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from ..items import RogJomaItem
import validators

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
        # priv_urls = len(self.urls)
        extracted_urls = set()
        for link in sel.xpath("//a/@href").getall():
            link = response.urljoin(link)
            # self.urls.add(link)
            if validators.url(link):
                extracted_urls.add(link)
        # print("[+] [bold green] Extracted URLS [bold cyan]",len(extracted_urls))
        # print(extracted_urls)
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
            # loader = ItemLoader(item=RogJomaItem(),response=response)

            sel = Selector(text=response.body)

            items=sel.xpath("//div[@class='product_cnt_border']").getall()
            for i in items:
                sel2=Selector(text=i)
                cijenaHRK = sel2.xpath("//span[@class='product_price_amount']/text()").get()
                cijenaEUR = sel2.xpath("//div[@class='productPriceEurTrans']/text()").get()
                url = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/@href").get()
                ime_artikla = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_name']/text()").get()
                kategorija = sel2.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_brand']/text()").get()
                slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@data-src").get()
                if slika is None:
                    slika = sel2.xpath("//div[@class='product_cnt_border']//picture/img/@src").get()

                item=RogJomaItem()
                item['Source']=response.url
                item['cijenaHRK']=cijenaHRK
                item['cijenaEUR']=cijenaEUR
                item['url']=url
                item['ime_artikla']=ime_artikla
                item['kategorija']=kategorija
                item['slika']=slika
                page = response.meta.get("playwright_page")
                await page.close()
                yield item
            



            # cijenaHRK = sel.xpath("//span[@class='product_price_amount']/text()").getall()
            # cijenaEUR = sel.xpath("//div[@class='productPriceEurTrans']/text()").getall()
            # url = sel.xpath("//div[@class='product_cnt_border']/div/h2/a/@href").getall()
            # ime_artikla = sel.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_name']/text()").getall()
            # kategorija = sel.xpath("//div[@class='product_cnt_border']/div/h2/a/span[@class='product_title_brand']/text()").getall()
            # slika = sel.xpath("//div[@class='product_cnt_border']//picture/img/@src").getall()

            # for idx, artikl in enumerate(ime_artikla):
            #     item=RogJomaItem()
            #     item['Source']=response.url
            #     item['cijenaHRK']=cijenaHRK[idx]
            #     item['cijenaEUR']=cijenaEUR[idx]
            #     item['url']=url[idx]
            #     item['ime_artikla']=ime_artikla[idx]
            #     item['kategorija']=kategorija[idx]
            #     item['slika']=slika[idx]

            #     page = response.meta.get("playwright_page")
            #     await page.close()
            #     yield item
        except:
            self.con.print_exception()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()