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

# make sure to check if they exist!!
# //span[contains(@class, "Sans-17px-black-85%-semibold")]    ## Get the first one ([0] or [1], not sure with xpath) and get text to get # of employees
# //span[contains(@class, "Sans-17px-black-85%-semibold")]/span[2]      ## Gets 3 elements for 6m growth, 1y growth, and 2y growth. still have to get text
                                                                        ## Format: XX% increse/decrease or "No change"
# table = driver.find_element_by_xpath('//table[@class="org-insights-functions-growth__table"]')    ## Get the employee distribution table
# Click functions????
#  //table[@class="org-insights-functions-growth__table"]/tr/td/div     ## Use .text to Get all table rows names (Sales, Engineering, etc.)
# //table[@class="org-insights-functions-growth__table"]/tr/td/span/span[2]  ## Use .text to Gets X% Increase/decrese for 6m and 1y. 2 per row
# //button[@aria-controls="ember8855-options"]      # The button to click to get those other things below
# //button[@class="org-insights-premium-dropdown__option-button"][@aria-pressed="false"]    ## Find the buttons to click. then do .click


## Get the company links from the spreadsheet
company_links = []
with open('C:/Users/abagh/CREtech_Full_List_Premium_Insights.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')
    for row in csv_reader:
            if len(row) == 0:
                company_links.append('')
            else:
                company_links.append(row[0])

## General Variables
running_males = 0
running_females = 0
running_unknown = 0
page_count = 0
male_names = []
female_names = []
unknown_names = []
csv_content = [['Company Link', 'Percent Male', 'Percent Female', 'Percent Unknown', '# Male', '# Female', '# Unknown', 'Unknown Names']]   # Add the names to an array
with open('male.txt') as f:
    male_names = f.readlines()  # get all names into an array
male_names = ([x.strip() for x in male_names])  # remove new line characters
male_names_set = set(male_names)
with open('female.txt') as f:
    female_names = f.readlines()  # get all names into an array
female_names = ([x.strip() for x in female_names])  # remove new line characters
female_names_set = set(female_names)

## Create the driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)  # To be used to detect if elements have loaded
driver.implicitly_wait(15)  # seconds

## Open the Linkedin page and login



def login_linkedin(your_username, your_password):
    driver.get(
        'https://www.linkedin.com/uas/login?session_redirect=%2Fvoyager%2FloginRedirect%2Ehtml&fromSignIn=true&trk=uno-reg-join-sign-in')  # Login page
    wait.until(EC.presence_of_element_located((By.ID, 'btn-primary')))  # Wait for the sign in button to load first
    login = driver.find_element_by_id('session_key-login')  # Get username box
    login.send_keys(your_username)  # Enter username
    password = driver.find_element_by_id('session_password-login')  # Get password box
    password.send_keys(your_password)  # Enter your password
    password.submit()
    print 'logged in: ' + your_username
    time.sleep(7)
    # Capcha
    if 'a quick security' in driver.page_source:
        time.sleep(30)
        waitInput = raw_input("Do the security check then press enter here")
        time.sleep(10)
    # When signing in from a new location
    if 'pin' in driver.page_source:
        pin = driver.find_element_by_id("verification-code")
        pin.send_keys(raw_input("Enter pin for: " + your_username))
        pin.submit()
        time.sleep(10)

##  Establish variables
page_string = '&page='  # Used to go to the next page manually via url parameters

# *************************************************************************** #
# ***************LOGIN TO ALL OF THEM IN YOUR VPN LOC TO AVOID PIN*********** #
# *************************************************************************** #
usernameArray = ['Your Email', 'Your Second Email Account (if you have one)']
passwordsArray = ['Your Password', 'Your Second Password']
# *************************************************************************** #
# *************************************************************************** #
# *************************************************************************** #
loginsUsed = 0
login_linkedin(usernameArray[loginsUsed], passwordsArray[loginsUsed])
storeCount = 0
for company_link in company_links:  # Loop through each link for each company
    if loginsUsed >= len(usernameArray):
        break
    if not company_link:    # If the company is a blank string
        csv_content.append([])
        continue
    pageSource = driver.page_source
    while 'No results found' in pageSource or 'account has been restricted' in pageSource:
        if 'No results found' in pageSource:
            print 'No results found' + usernameArray[loginsUsed]
        else:
            print 'Account Restricted: ' + usernameArray[loginsUsed]
        # Logout link
        driver.get(
            'https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_top%3BHd0EXRkpRdmjySf3ndvehg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_top-nav.settings_signout')
        time.sleep(8)
        loginsUsed += 1
        if loginsUsed >= len(usernameArray):
            break   # ultimate break, can't do anything anymore
        else:
            login_linkedin(usernameArray[loginsUsed], passwordsArray[loginsUsed])
            driver.get(company_link)  # Open up the employee page
            time.sleep(6)
            if 'No results found' in driver.page_source or 'account has been restricted' in driver.page_source:
                continue
            else:
                break
    if loginsUsed >= len(usernameArray):
        break
    employee_names = []  # Where their names will be stored
    driver.get(company_link)  # Open up the employee page
    time.sleep(uniform(3, 5))
    pageSource = driver.page_source
    while 'No results found' in pageSource or 'account has been restricted' in pageSource:
        if 'No results found' in driver.page_source:
            print 'No results found' + usernameArray[loginsUsed]
        else:
            print 'Account Restricted: ' + usernameArray[loginsUsed]
        # Logout link
        driver.get(
            'https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_top%3BHd0EXRkpRdmjySf3ndvehg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_top-nav.settings_signout')
        time.sleep(8)
        loginsUsed += 1
        if loginsUsed >= len(usernameArray):
            break   # ultimate break, can't do anything anymore
        else:
            login_linkedin(usernameArray[loginsUsed], passwordsArray[loginsUsed])
            driver.get(company_link)  # Open up the employee page
            time.sleep(6)
            if 'No results found' in driver.page_source or 'account has been restricted' in driver.page_source:
                continue
            else:
                driver.get(company_link)  # Open up the employee page
                time.sleep(uniform(3, 5))
                break
    if loginsUsed >= len(usernameArray):
        break
    try:
        page_text = driver.find_element_by_xpath('//h3[contains(@class, "search-results__total")]')  # Wait for the total search results box to load
    except (NoSuchElementException, TimeoutException):
        print 'Excepted: ' + company_link
        csv_content.append([company_link, 'Too long load time or no people found'])
        continue
    print page_text.text
    total_employees = page_text.text  # Gets the string for total number of employees
    # Format: Showing XXX results
    total_employees = total_employees.replace('Showing', '')
    total_employees = total_employees.replace('results', '')
    total_employees = total_employees.replace(' result', '')    # If it says only 1 result
    total_employees = total_employees.replace(',', '')
    if not total_employees:  # If the string is empty
        print 'No employee count for: ' + company_link
        csv_content.append([])
        continue
    total_employees = int(total_employees.strip())
    total_pages = int(math.ceil(total_employees / 10.0))  # 10 results per page
    time.sleep(uniform(.25, 4))  # Throttle
    for page_num in range(1, total_pages + 1):  # Go through each page for this company
        page_count += 1     # Debugging purposes
        print page_count
        driver.get(company_link + '&page=' + str(page_num))  # Go to the corresponding company page
        time.sleep(uniform(3, 9))  # Throttle
        pageSource = driver.page_source
        if 'No results found' in pageSource or 'account has been restricted' in pageSource:
            if 'No results found' in driver.page_source:
                print 'No results found: ' + usernameArray[loginsUsed]
            else:
                print 'Account Restricted: ' + usernameArray[loginsUsed]
            driver.save_screenshot('No results ' + str(page_num))
            # Logout link
            driver.get(
                'https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_top%3BHd0EXRkpRdmjySf3ndvehg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_top-nav.settings_signout')
            time.sleep(8)
            loginsUsed += 1
            if loginsUsed >= len(usernameArray):
                break
            else:
                login_linkedin(usernameArray[loginsUsed], passwordsArray[loginsUsed])
                raw_input('change your vpn to be safe, then press enter')
                continue
        if 'site cannot be' in driver.page_source or 'is no internet connection' in driver.page_source:
            time.sleep(100)
            dummy_text = raw_input('No internet')
            continue
        try:
            driver.find_elements_by_xpath('//div[@class="search-result__actions"]') # Wait for the "connect" button to load
        except (NoSuchElementException, TimeoutException):
            print 'should be no results found'
            continue
        driver.execute_script(
            "window.scrollTo(0, " + str((randint(300, 800))) + ");")  # Scroll down to the bottom of the page
        time.sleep(uniform(.5, 2))  # Throttle, allow content to load
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # Scroll down to the bottom of the page
        if total_pages <= 1:
            time.sleep(uniform(.1, 1.1))
        else:
            time.sleep(uniform(2, 4))
            try:
                driver.find_element_by_class_name('active')  # Wait until the page number bar at the bottom loads after scrolling
            except (NoSuchElementException, TimeoutException):
                print 'ip blocked?'
                print driver.page_source
                time.sleep(100)
                dummy_stall = raw_input('IP Blocked, change IP')
                continue
        for name in driver.find_elements_by_xpath(
                '//span[contains(@class, "actor-name")]'):  # Find all spans with class = "actor-name"
            employee_names.append(name.text)
        time.sleep(uniform(.5, 2))
        if len(driver.find_elements_by_xpath('//span[contains(@class, "actor-name")]')) == 0:
            storeCount += 1
        if storeCount >= 4:
            storeCount = 0
            driver.get('https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_top%3BHd0EXRkpRdmjySf3ndvehg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_top-nav.settings_signout')
            time.sleep(8)
            loginsUsed += 1
            if loginsUsed >= len(usernameArray):
                break
            else:
                login_linkedin(usernameArray[loginsUsed], passwordsArray[loginsUsed])
    if len(employee_names) >= 1:
        male_count = 0
        female_count = 0
        unknown_names = []
        for name in employee_names:
            name = name + ' '
            if len(set([name.split(' ', 1)[0].capitalize()]).intersection(male_names_set)) >= 1:
                male_count += 1
                running_males += 1
            elif len(set([name.split(' ', 1)[0].capitalize()]).intersection(female_names_set)) >= 1:
                female_count += 1
                running_females += 1
            else:
                unknown_names.append(name.encode('utf-8'))
                running_unknown += 1
        percent_male = (int(round(100 * male_count / len(employee_names))))
        percent_female = (int(round(100 * female_count / len(employee_names))))
        percent_unknown = 100 - (percent_female + percent_male)
        print 'Done with: ' + company_link
        print 'Percentage male: ' + str(percent_male)
        print 'Percentage female: ' + str(percent_female)
        print 'Percentage unknown: ' + str(percent_unknown)
        print unknown_names
        with open("C:/Users/abagh/results_for_special.csv", "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            csv_content.append(
                [company_link.encode('utf-8'), str(percent_male), str(percent_female), str(100 - (percent_female + percent_male)),
                 str(male_count), str(female_count), len(unknown_names), ', '.join(unknown_names)])
            for row in csv_content:
                writer.writerow(row)
    else:
        print 'not enough employees'
        csv_content.append([])  # Alignment
driver.close()
