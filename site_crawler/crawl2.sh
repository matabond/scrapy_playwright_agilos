#!/bin/bash
# get the start date and time
start_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_datetime} - starting spider rog_joma - debug: ${DEBUG}"

# go to venv directory
#activate venv
source /home/ubuntu/scrapy_playwright_example/venv_scraping/bin/activate

export NODE_OPTIONS=--max_old_space_size=32768

# prevent click, which pipenv relies on, from freaking out to due to lack of locale info https://click.palletsprojects.com/en/7.x/python3/
# export LC_ALL=en_US.utf-8

cd /home/ubuntu/scrapy_playwright_example/site_crawler
# run the spider
#scrapy crawl rog_joma -a debug=$DEBUG &> "logs/log_${start_datetime}.txt"
#timeout -k 5s 7200s scrapy crawl extreme_vital -a debug=$DEBUG &> "logs/log_ev${start_datetime}.txt" && echo OK || echo Failed, status $?

timeout -k 5s 7200s scrapy crawl rog_joma -a debug=$DEBUG &> "logs/log_rj${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part1 -a debug=$DEBUG &> "logs/log_bd1_${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part2 -a debug=$DEBUG &> "logs/log_bd2_${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part3 -a debug=$DEBUG &> "logs/log_bd3_${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part4 -a debug=$DEBUG &> "logs/log_bd4_${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part5 -a debug=$DEBUG &> "logs/log_bd5_${start_datetime}.txt" && echo OK || echo Failed, status $?

# timeout -k 5s 7200s scrapy crawl bike_discount_part6 -a debug=$DEBUG &> "logs/log_bd6_${start_datetime}.txt" && echo OK || echo Failed, status $?

# scrapy crawl novi -a debug=$DEBUG &> "logs/log_${start_datetime}.txt"

# get the end date and time
end_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${end_datetime} - spider finished successfully"cd ..