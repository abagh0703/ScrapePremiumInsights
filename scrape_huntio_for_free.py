from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import math
from random import *
import csv

csv_content = []
header_content = ['company_link']
master_array = []

## Get the company links from the spreadsheet
company_links = []
with open('C:/Users/abagh/RCA Master Links.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')
    for row in csv_reader:
            if len(row) == 0:
                company_links.append('')
            else:
                link = row[0].replace('http://', '')
                link = link.replace('https://', '')
                link = link.replace('www.', '')
                if '/' in link:
                    link = link.split('/', 1)[0]
                company_links.append('https://hunter.io/search/' + link)
print len(company_links)


def replace(your_list, to_replace, replacement):
    for n, i in enumerate(your_list):
        if n == to_replace:
            your_list[n]=replacement
            return your_list


def add_to_stats(header_name, value_to_insert):
    try:
        index = header_content.index(header_name)
        replace(company_stats, index, value_to_insert)
    except ValueError:
        header_content.append(header_name)
        index = header_content.index(header_name)
        replace(company_stats, index, value_to_insert)

## General Variables
search_count = 0


## Create the driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 6)  # To be used to detect if elements have loaded
driver.implicitly_wait(5)  # seconds

for company_link in company_links:  # Loop through each link for each company
    company_stats = []  # Where their names will be stored
    if company_link == '':    # If the company is a blank string
        add_to_stats('Error', 'No link')
        print 'no link'
        add_to_stats('company_link', 'None')
        master_array.append(company_stats)
        continue
    for i in range(100):
        company_stats.append('')
    driver.get(company_link)  # Open up the employee page
    search_count += 1
    if search_count % 145 == 0:
        dummy_stall = raw_input('change vpn, then press enter')
    add_to_stats('company_link', company_link)
    try:
        email_format = driver.find_element_by_xpath('//div[contains(@class, "search-pattern")]/strong').text  # Wait for the total search results box to load
        print email_format
        print search_count
        add_to_stats('email_format', email_format)
        master_array.append(company_stats)
    except (NoSuchElementException, TimeoutException, AttributeError):
        print 'No data for: ' + company_link
        add_to_stats('Error', 'No data')
        master_array.append(company_stats)
        continue
    if search_count % 20 == 0:
        with open("C:/Users/abagh/RCA_Formats.csv", "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(header_content)
            for row in master_array:
                writer.writerow(row)
with open("C:/Users/abagh/RCA Formats.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(header_content)
    for row in master_array:
        writer.writerow(row)
print 'done!!!'