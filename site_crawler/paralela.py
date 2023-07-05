from site_crawler.spiders.extreme_vital import BikeSpider2
from site_crawler.spiders.rog_joma import Rog_Joma_Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    settings=get_project_settings()
    process= CrawlerProcess(settings)
    process.crawl(BikeSpider2)
    process.crawl(Rog_Joma_Spider)
    process.start()


if __name__ == '__main__':
    main()