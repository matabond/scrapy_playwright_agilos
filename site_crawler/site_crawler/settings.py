# Scrapy settings for site_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'site_crawler'

SPIDER_MODULES = ['site_crawler.spiders']
NEWSPIDER_MODULE = 'site_crawler.spiders'

LOG_LEVEL = 'ERROR'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'site_crawler (+http://www.yourdomain.com)'
from .utils import get_random_agent, should_abort_request

USER_AGENT = get_random_agent()

# PLAYWRIGHT_ABORT_REQUEST = should_abort_request #AttributeError: 'Request' object has no attribute 'resourceType'

PLAYWRIGHT_BROWSER_TYPE = "chromium" #firefox
PLAYWRIGHT_ABORT_REQUEST = should_abort_request #AttributeError: 'Request' object has no attribute 'resourceType' - riješeno


MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'bikedb'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8  #je li ovo Matija dodavao? Zasto nije default - zbog memorije?
MEMDEBUG_ENABLED=True


#autothrottle

# DOWNLOAD_DELAY = 2  # minimum download delay 
AUTOTHROTTLE_ENABLED = True

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'site_crawler.middlewares.SiteCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'site_crawler.middlewares.SiteCrawlerDownloaderMiddleware': 543,
# }

"""
Place this line of code at the top of your settings.py file, along with other settings for your Scrapy project. 
The CLOSESPIDER_PAGECOUNT setting sets the number of pages that the Scrapy spider will scrape before shutting down automatically. 
In this example, the spider will stop after scraping 1000 pages.
"""
# CLOSESPIDER_PAGECOUNT=1000

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.closespider.CloseSpider.CLOSESPIDER_PAGECOUNT': None,
# }

MEMUSAGE_LIMIT_MB=0

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'site_crawler.pipelines.MongoPipeline': 300
    'site_crawler.pipelines.PostgresPipeline_bike': 100
    # 'site_crawler.pipelines.PostgresPipeline': 100
}

HTTPERROR_ALLOW_ALL=True  # ako slucajno naleti na stranicu s ovom greskom
#CLOSESPIDER_TIMEOUT = 5 * 60 * 60  #zatvori spider nakon 3 sata
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 0  # Timeout to be used when requesting pages by Playwright, default is 30, pokusala i sa 100 no onda timeout 1000000
DUPEFILTER_DEBUG = True  #to help with debug
DOWNLOAD_TIMEOUT = 10   #default je 180, u knjizi preporucaju smanjiti na 10 sekundi ako postoji timeout problem, reduce the download timeout so that stuck requests are discarded quickly and free up capacity to process the next ones.
RETRY_ENABLED = False   #Retrying failed HTTP requests can slow down the crawls substantially, specially when sites causes are very slow (or fail) to respond, thus causing a timeout error which gets retried many times, unnecessarily, preventing crawler capacity to be reused for other domains.
COOKIES_ENABLED = False  #mozda malo pomogne, ne znam,  Cookies are often not needed

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
