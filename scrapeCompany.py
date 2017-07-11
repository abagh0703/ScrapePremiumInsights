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


## Create the driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)    # To be used to detect if elements have loaded
driver.implicitly_wait(5)  # seconds

## Open the Linkedin page and login
driver.get('https://www.linkedin.com/uas/login?session_redirect=%2Fvoyager%2FloginRedirect%2Ehtml&fromSignIn=true&trk=uno-reg-join-sign-in')    # Login page
wait.until(EC.presence_of_element_located((By.ID, 'btn-primary')))   # Wait for the sign in button to load first
login = driver.find_element_by_id('session_key-login')  # Get username box
login.send_keys('bharatunian@gmail.com')  # Enter username
password = driver.find_element_by_id('session_password-login')  # Get password box
password.send_keys('bharatunian')    # Enter your password
password.submit()
time.sleep(5)

# pin = driver.find_element_by_id("verification-code")
# pin.send_keys(raw_input("Enter pin"))
# pin.submit()

# time.sleep(5)

##  Establish variables
page_string = '&page='  # Used to go to the next page manually via url parameters
company_links = ['https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%222612274%22%5D',
                 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%223338049%22%5D']  # Array of Linkedin company employee pages, as strings. Do not include the &page paramter!

for company_link in company_links:  # Loop through each link for each company
    employee_names = []     # Where their names will be stored
    driver.get(company_link)    # Open up the employee page
    page_text = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//h3[contains(@class, "search-results__total")]')))  # Wait for the total search rseults box to load
    total_employees = page_text.text    # Gets the string for total number of employees
    # Format: Showing XXX results
    total_employees = total_employees.replace('Showing', '')
    total_employees = total_employees.replace('results', '')
    total_employees = total_employees.replace(',', ' ')
    total_employees = int(total_employees.strip())
    # 10 results per page
    total_pages = int(math.ceil(total_employees/10))
    for page_num in range(1, total_pages):  # Go through each page for this company
        driver.get(company_link + '&page=' + str(page_num))  # Go to the corresponding company page
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="search-result__actions"]')))  # Wait for the connect button to load
        driver.execute_script(
            "window.scrollTo(0, 500);")  # Scroll down to the bottom of the page
        time.sleep(.65)     # allow content to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll down to the bottom of the page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'active')))   # Wait until the page number bar at the bottom loads after scrolling
        for name in driver.find_elements_by_xpath('//span[contains(@class, "actor-name")]'):   # Find all spans with class = "actor-name"
            employee_names.append(name.text)
        if page_num == 3:
            break
    print 'Done with: ' + company_link
    male_names = []
    female_names = []
    unknown_names = []
    with open('male.txt') as f:
        male_names = f.readlines()  # get all names into an array
    male_names = [x.strip() for x in male_names]  # remove new line characters
    with open('female.txt') as f:
        female_names = f.readlines()  # get all names into an array
    female_names = [x.strip() for x in female_names]  # remove new line characters
    male_count = 0
    female_count = 0
    for name in employee_names:
        if name.split(' ', 1)[0].capitalize() in male_names:
            male_count += 1
        elif name.split(' ', 1)[0].capitalize() in female_names:
            female_count += 1
        else:
            unknown_names.append(name)
    percent_male = (int(round(100 * male_count / len(employee_names))))
    percent_female = (int(round(100 * female_count / len(employee_names))))
    print 'Percentage male: ' + str(percent_male)
    print 'Percentage female: ' + str(percent_female)
    print 'Percentage unkown: ' + str(100 - (percent_female + percent_male))
    print unknown_names
driver.close()

