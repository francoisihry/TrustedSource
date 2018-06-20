#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author : Francois Ihry (github:francoisihry)

import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TRUSTED_SOURCE_URL = "https://www.trustedsource.org/en/feedback/url"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",
        help=("The url you want to submit to TrustedSource."),required=True)
    parser.add_argument('--headless', help='Will launch Firefox in headless mode',
                        action='store_true')
    return parser.parse_args()


def trusted_source():
    args = parse_args()
    print("Submitting {} to TrustedSource...".format(args.url))
    options = Options()
    if args.headless:
        print("In headless mode...")
        options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.wait = WebDriverWait(driver, 90)
    driver.get(TRUSTED_SOURCE_URL)
    product = Select(driver.find_element_by_name('product'))
    product.select_by_value('15-xl')
    url = driver.find_element_by_name("url")
    url.send_keys(args.url)
    check_url_button = driver.find_element_by_xpath("//input[@value='Check URL']")
    check_url_button.click()
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'result-table'))
    WebDriverWait(driver, 20).until(element_present)
    soup = BeautifulSoup(driver.page_source, "html5lib")
    result_table = soup.find("table", {"class": "result-table"})
    rows = list()
    for row in result_table.findAll("tr"):
        cols = list()
        for col in row.findAll("td"):
            cols.append(col)
        rows.append(cols)
    url = rows[1][1].text
    status = rows[1][2].text
    category = rows[1][3].text
    reputation = rows[1][4].text
    print("url : {}".format(url))
    print("status : {}".format(status))
    print("category : {}".format(category))
    print("reputation : {}".format(reputation))
    driver.close()


if __name__ == "__main__" :
    trusted_source()
