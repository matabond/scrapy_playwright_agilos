# scrapy_playwright_example
This repo contains a scraping script that crawls a JavaScript-rendered webpage using the scrapy-playwright package in Python and the scrapy framework

# Objective of the Project
I created this script to test the **scrapy-playwright** python package in crawling a JavaScript rendered [webpage](https://www.disco.com.ar/panales-pampers-confortsec-pequeno-x56/p). 

![image](https://user-images.githubusercontent.com/98691360/193428986-9030d8a7-9d2a-463b-af3f-b6c5cd4527ca.png)

To scrape dynamic websites in Python, one of these three options can be used:
- **scrapy-playwright**
- **scrapy-splash** (requires **Docker**)
- A **proxy service** that has a built-in JS rendering capability (e.g., [Zyte Smart Proxy Manager](https://www.zyte.com/smart-proxy-manager/) or [ScraperAPI](https://www.scraperapi.com/documentation/python/)).

I prefer option #1 for low-volume scraping and option #3 for high-volume scraping because these proxy services also re-route your requests and overcome the anti-bot mechanisms that E-commerce websites use. Option #2 also works pretty well, but you need to be familiar with docker and have it installed on your computer. scrapy-playwright does not need a docker-image to work and acts as a direct plugin to scrapy, which makes it pretty easy to use.

# Usability and Reproducability
**Step 1:** scrapy-playwright does **not work natively on Windows**. It only works on **Linux** and **Mac**. If you use Windows, you'll need to use Windows Subsystem for Linux (WSL). Otherwise, the spider will always fail.

If you are using Windows, please follow the steps in this [video](https://youtu.be/QGSz6KvsDSI?t=272) from 4:30 to 14:00 to install **WSL**, **VSCode**, and **Windows Terminal** on your machine. The video is courtesy of YouTube user **freakingud**. It is **not** in English (probably Hindi), but you will be able to follow the steps without any problems from the screen recordings. I found this to be one of the most straightforward guides to install WSL despite the fact that I did not understand the language.

After installing WSL, you will need to do two additional steps:
- **Upgrade it from WSL1 to WSL2**. To do this, follow the steps in this [guide](https://dev.to/adityakanekar/upgrading-from-wsl1-to-wsl2-1fl9)
- **Install the VSCode extentions** shown in the image below. The ones that are specifically needed for WSL to work are **WSL**, **Pylance**, and **Python**, but the others are pretty useful for other use cases, and I recommend you keep them in your standard toolbox 

![image](https://user-images.githubusercontent.com/98691360/193427758-352b83e3-70d5-4366-9377-e21238f04215.png)
_**Note 1:** You will need to install these extensions again in the **WSL: Ubuntu** environment once you connect to the WSL remote container (steps explained below)_
_**Note 2:** The name of the distro in the ```wsl --set-version <distro-name> 2``` step is Ubuntu_

**Step 2:** From VSCode, click on the **green/purple icon** in the **bottom left hand corner**, then click on **New WSL Window using Distro**, and finally **Ubuntu**

![image](https://user-images.githubusercontent.com/98691360/193428126-c1a44b84-72d1-4e2f-9374-210a9942e975.png)

You should land on a page that looks like this

![image](https://user-images.githubusercontent.com/98691360/193428259-0d7d6295-6079-4d5e-929c-ba116a1d04dc.png)

**Step 3:** Open your terminal and type in ```git clone https://github.com/omar-elmaria/scrapy_playwright_example.git```

**Step 4:** After the repo is cloned, type ```cd scrapy_playwright_example``` in your terminal, then ```python -m venv venv_scraping``` to create a virtual environment

**Step 5:** Activate the virtual environment by typing ```source venv_scraping/bin/activate```

**Step 6:** Type ```pip3 install -r requirements.txt``` to install the dependencies

**Step 7:** If it is your first time using scrapy-playwright, you will also need to install the headless browsers by typing ```playwright install``` in your terminal

**Step 8:** Before running the crawler, please enter the following lines in your ```settings.py``` file
```
# Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
```

This comes directly from the [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright) official documentation. I encourage you to go through it to get acquainted with more use cases of the plugin.

**Step 9:** To run the crawler, type ```cd scrapy_playwright_example/site_crawler``` in your terminal and then enter the following command --> ```scrapy crawl spanish_site_crawler```. This will launch the spider and crawl the **product name**, **discount tag**, and **price** of the product. **spanish_site_crawler_terminal** is the name of the spider and can be changed by setting the variable ```name``` under the ```SiteCrawlerSpider``` class to something else

The end result should look like this...

![image](https://user-images.githubusercontent.com/98691360/193428966-f634628d-8681-4614-a48b-7460f3794442.png)

**Step 10 (Optional):** If you want to launch the spider by running the script itself through the **play** button at the top right hand corner and **not** through the terminal, please add the following import command at the start of the script ```from scrapy.crawler import CrawlerProcess``` and insert these few lines of code at the end of the script **without indentation outside the class code block**
```
process = CrawlerProcess(settings = {
    "DOWNLOAD_HANDLERS": {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    },

    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
}) # The same lines of code you put in settings.py
process.crawl(SiteCrawlerSpider) # Name of the class
process.start()
```

# Extra Resources
Here are two nice YouTube videos that walk you through how to install and use the package:
- A [tutorial](https://www.youtube.com/watch?v=0wO7K-SoUHM) by John Watson Rooney
- A [tutorial](https://www.youtube.com/watch?v=VDpi9cwgiR8) by Upendra
