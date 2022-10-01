# scrapy_playwright_example
This repo contains a scraping script that crawls a JavaScript-rendered webpage using the scrapy-playwright package in Python and the scrapy framework

# Objective of the Project
I created this script to test the **scrapy-playwright** python package in crawling a JavaScript rendered [webpage](https://www.disco.com.ar/panales-pampers-confortsec-pequeno-x56/p). To scrape dynamic websites in Python, one of these three options can be used:
- scrapy-playwright
- scrapy-splash (requires **Docker**)
- A proxy service that has a built-in JS rendering capability (e.g., [Zyte Smart Proxy Manager](https://www.zyte.com/smart-proxy-manager/) or [ScraperAPI](https://www.scraperapi.com/documentation/python/)).

I prefer option #1 for low-volume scraping and option #3 for high-volume scraping because these proxy services also re-route your requests and overcome the anti-bot mechanisms that E-commerce websites use. Option #2 also works pretty well, but you need to be familiar with docker and have it installed on your computer. scrapy-playwright does not need a docker-image to work and acts as a direct plugin to scrapy, which makes it pretty easy to use.

# Usability and Reproducability
1. scrapy-playwright does **not work natively on Windows**. It only works on **Linux** and **Mac**. If you use Windows, you'll need to use Windows Subsystem for Linux (WSL). Otherwise, the spider will always fail.

If you are using Windows, please follow the steps in this [video](https://youtu.be/QGSz6KvsDSI?t=272) from 4:30 to 14:00 to install **WSL**, **VSCode**, and **Windows Terminal** on your machine. The video is courtesy of YouTube user **freakingud**. It is **not** in English (probably Hindi), but you will be able to follow the steps without any problems from the screen recordings. I found this to be one of the most straightforward guides to install WSL despite the fact that I did not understand the language.

After installing WSL, you will need to do two additional steps:
- Upgrade it from WSL1 to WSL2. To do this, follow the steps in this [guide](https://dev.to/adityakanekar/upgrading-from-wsl1-to-wsl2-1fl9)
- Install the VSCode extentions shown in the image below. The ones that are specifically needed for WSL to work are **WSL**, **Pylance**, and **Python**, but the others are pretty useful for other use cases, and I recommend you keep them in your standard toolbox 

![image](https://user-images.githubusercontent.com/98691360/193427758-352b83e3-70d5-4366-9377-e21238f04215.png)
_**Note 1:** You will need to install these extensions again in the **WSL: Ubuntu** environment once you connect to the WSL remote container (steps explained below)_
_**Note 2:** The name of the distro in the ```wsl --set-version <distro-name> 2``` step is Ubuntu_

2. From VSCode, click on the **green/purple icon** in the **bottom left hand corner**, then click on **New WSL Window using Distro**, and finally **Ubuntu**

![image](https://user-images.githubusercontent.com/98691360/193428126-c1a44b84-72d1-4e2f-9374-210a9942e975.png)

You should land on a page that looks like this

![image](https://user-images.githubusercontent.com/98691360/193428184-68a5abfe-25c0-486e-b595-c762ebce18d9.png)

3. Open your terminal and type in ```git clone {}```


# Extra Resources
Here are two nice YouTube videos that walk you through how to install and use the package:
- A [tutorial](https://www.youtube.com/watch?v=0wO7K-SoUHM) by John Watson Rooney
- A [tutorial](https://www.youtube.com/watch?v=VDpi9cwgiR8) by Upendra
