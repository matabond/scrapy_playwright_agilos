#!/bin/bash
# get the start date and time
start_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_datetime} - starting spider rog_joma - debug: ${DEBUG}"

# go to venv directory
#activate venv
source /home/ubuntu/scrapy_playwright_example/venv_scraping/bin/activate

# prevent click, which pipenv relies on, from freaking out to due to lack of locale info https://click.palletsprojects.com/en/7.x/python3/
# export LC_ALL=en_US.utf-8

cd /home/ubuntu/scrapy_playwright_example/site_crawler
# run the spider
scrapy crawl rog_joma -a debug=$DEBUG &> "logs/log_${start_datetime}.txt"

# get the end date and time
end_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${end_datetime} - spider finished successfully"