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

# //div[contains(@class, "org-insights-module__facts")]

csv_content = []
# header_content = []   # Add the names to an array 'Total Employees', '6 Month Growth', '1 Year Growth', '2 Year Growth'
header_content = ['company_link', 'company_name', u'General total employees', u'General 6m growth', u'General 1y growth', u'General 2y growth', u'Headcount growth Sales_6m', u'Headcount growth Sales_1y', u'Headcount growth Engineering_6m', u'Headcount growth Engineering_1y', u'Headcount growth Business Development_6m', u'Headcount growth Business Development_1y', u'Headcount growth Information Technology_6m', u'Headcount growth Information Technology_1y', u'Headcount growth Arts and Design_6m', u'Headcount growth Arts and Design_1y', u'Headcount growth Entrepreneurship_6m', u'Headcount growth Entrepreneurship_1y', u'Headcount growth Finance_6m', u'Headcount growth Finance_1y', u'Headcount growth Human Resources_6m', u'Headcount growth Human Resources_1y', u'Headcount growth Marketing_6m', u'Headcount growth Marketing_1y', u'Headcount growth Media and Communication_6m', u'Headcount growth Media and Communication_1y', u'Headcount growth Operations_6m', u'Headcount growth Operations_1y', u'Headcount growth Product Management_6m', u'Headcount growth Product Management_1y', u'Headcount growth Program and Project Management_6m', u'Headcount growth Program and Project Management_1y', u'Headcount growth Quality Assurance_6m', u'Headcount growth Quality Assurance_1y', u'Headcount growth Support_6m', u'Headcount growth Support_1y', u'Job openings growth Sales_3m', u'Job openings growth Sales_6m', u'Job openings growth Sales_1y', u'Job openings growth Accounting_3m', u'Job openings growth Accounting_6m', u'Job openings growth Accounting_1y', u'Job openings growth Engineering_3m', u'Job openings growth Engineering_6m', u'Job openings growth Engineering_1y', u'Job openings growth Arts and Design_3m', u'Job openings growth Arts and Design_6m', u'Job openings growth Arts and Design_1y', u'Job openings growth Business Development_3m', u'Job openings growth Business Development_6m', u'Job openings growth Business Development_1y', u'Job openings growth Finance_3m', u'Job openings growth Finance_6m', u'Job openings growth Finance_1y', u'Job openings growth Information Technology_3m', u'Job openings growth Information Technology_6m', u'Job openings growth Information Technology_1y', u'Job openings growth Marketing_3m', u'Job openings growth Marketing_6m', u'Job openings growth Marketing_1y', u'Job openings growth Support_3m', u'Job openings growth Support_6m', u'Job openings growth Support_1y', u'Job openings growth Other_3m', u'Job openings growth Other_6m', u'Job openings growth Other_1y', u'Headcount growth Administrative_6m', u'Headcount growth Administrative_1y', u'Headcount growth Legal_6m', u'Headcount growth Legal_1y', u'Headcount growth Research_6m', u'Headcount growth Research_1y', u'Job openings growth Research_3m', u'Job openings growth Research_6m', u'Job openings growth Research_1y', u'Headcount growth Community and Social Services_6m', u'Headcount growth Community and Social Services_1y', u'Headcount growth Accounting_6m', u'Headcount growth Accounting_1y', u'Headcount growth Consulting_6m', u'Headcount growth Consulting_1y', u'Job openings growth Human Resources_3m', u'Job openings growth Human Resources_6m', u'Job openings growth Human Resources_1y', 'Error', u'Headcount growth Real Estate_6m', u'Headcount growth Real Estate_1y', u'Job openings growth Education_3m', u'Job openings growth Education_6m', u'Job openings growth Education_1y', u'Job openings growth Legal_3m', u'Job openings growth Legal_6m', u'Job openings growth Legal_1y', u'Job openings growth Media and Communication_3m', u'Job openings growth Media and Communication_6m', u'Job openings growth Media and Communication_1y', u'Job openings growth Real Estate_3m', u'Job openings growth Real Estate_6m', u'Job openings growth Real Estate_1y', u'Job openings growth Operations_3m', u'Job openings growth Operations_6m', u'Job openings growth Operations_1y', u'Job openings growth Administrative_3m', u'Job openings growth Administrative_6m', u'Job openings growth Administrative_1y', u'Job openings growth Entrepreneurship_3m', u'Job openings growth Entrepreneurship_6m', u'Job openings growth Entrepreneurship_1y', u'Job openings growth Product Management_3m', u'Job openings growth Product Management_6m', u'Job openings growth Product Management_1y', u'Job openings growth Program and Project Management_3m', u'Job openings growth Program and Project Management_6m', u'Job openings growth Program and Project Management_1y', u'Headcount growth Education_6m', u'Headcount growth Education_1y', u'Job openings growth Quality Assurance_3m', u'Job openings growth Quality Assurance_6m', u'Job openings growth Quality Assurance_1y', u'Headcount growth Purchasing_6m', u'Headcount growth Purchasing_1y', u'Job openings growth Consulting_3m', u'Job openings growth Consulting_6m', u'Job openings growth Consulting_1y']
master_array = []

## Get the company links from the spreadsheet
company_links = []
with open('C:/Users/abagh/CREtech_Full_Trial_2.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')
    for row in csv_reader:
            if len(row) == 0:
                company_links.append('')
                print ''
            elif 'company-beta' in row[0]:
                company_links.append(row[0])
                print row[0]
            else:
                company_id = row[0].replace('https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22', '')  # get only the id
                company_id = company_id.replace('%22%5D', '')   # again removing unnecessary stuff
                company_links.append('https://www.linkedin.com/company-beta/' + company_id + '/')
                print 'https://www.linkedin.com/company-beta/' + company_id + '/'
print len(company_links)

def clean_growth(raw_growth):
    raw_growth = raw_growth.replace(',', '')
    raw_growth = raw_growth.replace('No change', '0')
    raw_growth = raw_growth.replace('% increase', '')
    raw_growth = raw_growth.replace('% decrease', '')
    if '%' in raw_growth:
        raw_growth = raw_growth.split('\n')[1]
    return int(raw_growth.strip())


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
page_count = 0


## Create the driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 6)  # To be used to detect if elements have loaded
driver.implicitly_wait(8)  # seconds

## Open the Linkedin page and login
driver.get(
    'https://www.linkedin.com/uas/login?session_redirect=%2Fvoyager%2FloginRedirect%2Ehtml&fromSignIn=true&trk=uno-reg-join-sign-in')  # Login page
wait.until(EC.presence_of_element_located((By.ID, 'btn-primary')))  # Wait for the sign in button to load first

login = driver.find_element_by_id('session_key-login')  # Get username box
login.send_keys('')  # Enter username
password = driver.find_element_by_id('session_password-login')  # Get password box
password.send_keys('')  # Enter your password
password.submit()
time.sleep(7)

driver_source = driver.page_source
if 'pin' in driver_source:
    pin = driver.find_element_by_id("verification-code")
    pin.send_keys(raw_input("Enter pin"))
    pin.submit()
    time.sleep(10)

if 'a quick security' in driver_source:
    raw_input("A quick security check")
    time.sleep(30)
## When signing in from a new location
# pin = driver.find_element_by_id("verification-code")
# pin.send_keys(raw_input("Enter pin"))
# pin.submit()
# time.sleep(10)
for company_link in company_links:  # Loop through each link for each company
    company_stats = []  # Where their names will be stored
    if company_link == '':    # If the company is a blank string
        add_to_stats('Error', 'No link')
        add_to_stats('company_link', 'None')
        master_array.append(company_stats)
        continue
    for i in range(100):
        company_stats.append('')
    driver.get(company_link)  # Open up the employee page
    try:
        company_name = driver.find_element_by_xpath('//h1[contains(@class, "org-top-card-module__name")]')  # Wait for the total search results box to load
    except (NoSuchElementException, TimeoutException):
        print 'Excepted: ' + company_link
        add_to_stats('Error', 'Loading took too long')
        add_to_stats('company_link', company_link)
        time.sleep(120)
        master_array.append(company_stats)
        continue
    add_to_stats('company_link', company_link)
    add_to_stats('company_name', company_name.text.encode('utf-8'))
    time.sleep(uniform(2, 5))  # Throttle
    driver.execute_script(
        "window.scrollTo(0, " + str((randint(900, 1000))) + ");")  # Scroll down to the mid page
    time.sleep(uniform(2, 4))  # Throttle, allow content to load
    try:    # employee headcount
        # employee_count = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "Sans-17px-black-85%-semibold")]')))  # Wait for the total search results box to load
        # employee_count = employee_count[0].text
        # # add_to_stats('employee_count', employee_count)
        test_for_basics = driver.find_element_by_xpath('//table[contains(@class, "org-insights-module__summary-table")]/tr[1]')
        employee_growth = driver.find_elements_by_xpath('//table[contains(@class, "org-insights-module__summary-table")]/tr[1]/td')
        values = []
        for td in employee_growth:
            values.append(clean_growth(td.text))
        employee_growth_names = driver.find_elements_by_xpath('//table[contains(@class, "org-insights-module__summary-table")]/tr[2]/th')
        for i in range(0, len(employee_growth_names)):
            add_to_stats('General ' + employee_growth_names[i].text, values[i])
    except (NoSuchElementException, TimeoutException):
        pass
    try:    # employee distribution
        button = driver.find_element_by_xpath('//button[contains(@class, "org-insights-premium-dropdown__trigger")]')    ## Get the employee distribution table
        button.send_keys(webdriver.common.keys.Keys.SPACE)
        employee_distributions = driver.find_elements_by_xpath('//button[@class="org-insights-premium-dropdown__option-button"][@aria-pressed="false"]')
        for distribution in employee_distributions:
            distribution.send_keys(webdriver.common.keys.Keys.SPACE)  # Show all items in table
            time.sleep(uniform(.25, .4))
        first_table = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[0]
        distribution_growth_percentages = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[0].find_elements_by_xpath('tr/td/span/span[2]')
        distribution_growth_array = []
        for percentage in distribution_growth_percentages:
            distribution_growth_array.append(clean_growth(percentage.text))
        distribution_growth_names = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[0].find_elements_by_xpath('tr/th')
        category_name = distribution_growth_names.pop(0)  # 6m, 1y, and/or 2y
        job_openings_names = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[0].find_elements_by_xpath('tr/td/div')
        number_of_time_categories = len(distribution_growth_names)
        for i in range(len(job_openings_names)):
            if number_of_time_categories >= 1:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[0].text.encode('utf-8'), (distribution_growth_array[i * number_of_time_categories]))
            if number_of_time_categories >= 2:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[1].text.encode('utf-8'), distribution_growth_array[i * number_of_time_categories + 1])
            if number_of_time_categories >= 3:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[2].text.encode('utf-8'), distribution_growth_array[i * number_of_time_categories + 2])
    except (NoSuchElementException, TimeoutException):
        pass
    time.sleep(uniform(2, 4))
    try:    # job openings
        driver.execute_script(
            "window.scrollTo(0, " + str((randint(3100, 3200))) + ");")  # Scroll down to the bottom of the page
        time.sleep(uniform(3, 5))
        button = driver.find_elements_by_xpath('//button[contains(@class, "org-insights-premium-dropdown__trigger")]')    ## Get the employee distribution table
        if len(button) < 2:     # Meaning it doesn't have the other graph
            raise NoSuchElementException
        button = button[1]  # Second button on page
        button.send_keys(webdriver.common.keys.Keys.SPACE)
        employee_distributions = driver.find_elements_by_xpath('//button[@class="org-insights-premium-dropdown__option-button"][@aria-pressed="false"]')
        for distribution in employee_distributions:
            distribution.send_keys(webdriver.common.keys.Keys.SPACE)   # Show all items in table
            time.sleep(uniform(.25, .4))
        second_table = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[1]
        distribution_growth_percentages = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[1].find_elements_by_xpath('tr/td/span/span[2]')
        distribution_growth_array = []
        for percentage in distribution_growth_percentages:
            distribution_growth_array.append(clean_growth(percentage.text))
        distribution_growth_names = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[1].find_elements_by_xpath('tr/th')
        category_name = distribution_growth_names.pop(0)    # 6m, 1y, and/or 2y
        job_openings_names = driver.find_elements_by_xpath('//table[@class="org-insights-functions-growth__table"]')[1].find_elements_by_xpath('tr/td/div')
        number_of_time_categories = len(distribution_growth_names)
        for i in range(len(job_openings_names)):
            if number_of_time_categories >= 1:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[0].text.encode('utf-8'), (distribution_growth_array[i * number_of_time_categories]))
            if number_of_time_categories >= 2:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[1].text.encode('utf-8'), distribution_growth_array[i * number_of_time_categories + 1])
            if number_of_time_categories >= 3:
                add_to_stats(category_name.text + ' ' + job_openings_names[i].text + '_' + distribution_growth_names[2].text.encode('utf-8'), distribution_growth_array[i * number_of_time_categories + 2])
    except (NoSuchElementException, TimeoutException):
            pass
    print company_stats
    print header_content
    with open("C:/Users/abagh/results_company_pages.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        master_array.append(company_stats)
        writer.writerow(header_content)
        for row in master_array:
            writer.writerow(row)
print 'done!!!'
driver.close()
