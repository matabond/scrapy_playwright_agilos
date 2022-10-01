import scrapy
from scrapy_playwright.page import PageMethod

class SiteCrawlerSpider(scrapy.Spider):
    name = 'spanish_site_crawler'
    start_urls = ['https://www.disco.com.ar/panales-pampers-confortsec-pequeno-x56/p']

    def start_requests(self):
        yield scrapy.Request(
            url = "https://www.disco.com.ar/panales-pampers-confortsec-pequeno-x56/p",
            meta = {
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.discoargentina-store-theme-tha9pV36seWfdnuHGKz68")
                ],
                "errback": self.errback,
            }
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        product_name = response.xpath(".//span[contains(@class, 'vtex-store-components-3-x-productBrand')]/text()")
        discount_selector = response.xpath(".//p[@title = 'FS_40%_PANALES | Descuento por Estructura']/text()")
        # discount_selector = response.css("p[title='FS_40%_PANALES | Descuento por Estructura']::text") # The previous selector but with css instead of xpath
        price_selector = response.xpath(".//div[@class = 'contenedor-precio']")
        yield {
            "product_name": product_name.get(),
            "price": price_selector.xpath('.//span/text()').get(),
            "product_discount": discount_selector.get(),
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()