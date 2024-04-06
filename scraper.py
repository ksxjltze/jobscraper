from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import csv

options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)

options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

import time;
import random;

BASE_URL = 'https://sg.indeed.com/jobs'
QUERY = '?q=software+engineer&l=Singapore'

driver = webdriver.Chrome()
driver.get(BASE_URL + QUERY)
driver.maximize_window()

title = driver.title
wait = WebDriverWait(driver, 10)

acceptCookiesButtonLocator = (By.ID, "onetrust-accept-btn-handler")
wait.until(EC.element_to_be_clickable(acceptCookiesButtonLocator)).click()

jobs_data = []

PAGES = 999
currentPage = 0

SAVE_INTERVAL = 5 * 15
jobsCounted = 0

def clamp(x, a, b):
    return max(a, min(x, b))

def sleep_random(min_sleep_time, max_sleep_time): 
    sleep_time = random.random() * max_sleep_time
    sleep_time_clamped = clamp(sleep_time, min_sleep_time, max_sleep_time)
    
    time.sleep(sleep_time_clamped)
    
def write_to_csv():
    with open('jobs.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        headers = ['Title', 'Company', 'Pay', 'Description', "Type"]
        writer.writerow(headers)
        
        for job in jobs_data:
            writer.writerow(iter(job))
        
        jobs_data.clear()
        csvfile.close()
    
def finalize():
    print("FINALIZING")       
    write_to_csv()
    
    driver.quit()       
    exit()

try:
    while currentPage < PAGES:
        jobs = driver.find_elements(By.CLASS_NAME, "tapItem")
        for job in jobs:
            errors = [NoSuchElementException]
            
            wait.until(EC.element_to_be_clickable(job))
            job.click()
            sleep_random(3, 6)
            
            try:
                jobPane = driver.find_element(By.ID, "jobsearch-ViewjobPaneWrapper")
                
            except Exception as e:
                print(e)
                
                try:
                    skeletonLocator = (By.XPATH, "//div[@data-testid='viewJob-skeleton']")
                    wait.until(EC.presence_of_element_located(skeletonLocator))
                    
                except Exception as e2:
                    print(e2)
                    finalize()
                    break
            
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jobsearch-JobInfoHeader-title")))
            
            jobTitle = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "span")
            companyInfo = job.find_element(By.CLASS_NAME, "company_location")
            companyName = companyInfo.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
            
            jobTitleText = ""
            jobDescription = ""
            jobInfoText = ""
            payText = ""
            companyNameText = ""
            
            try:
                jobDescription = jobPane.find_element(By.ID, "jobDescriptionText").text
                
            except Exception as e:
                jobDescription = "NA"
            
            jobTitleText = jobTitle.text.strip()
            companyNameText = companyName.text.strip()
            
            try:
                try:
                    infoAndJobTypeElement = jobPane.find_element(By.ID, "salaryInfoAndJobType")
                    jobInfoText = infoAndJobTypeElement.text
                    
                except Exception as e2:
                    print("No job info found: " + jobTitle.text.strip() + " (" + companyName.text.strip() + ")")
                    jobInfoText = "NA"
                
                payElement = jobPane.find_element(By.CSS_SELECTOR, "div[aria-label='Pay']")
                payText = payElement.text.strip().removeprefix("Pay\n")
                print(payText + ": (" + jobTitleText + ")" + " - " + companyNameText)
                
            except Exception as e:
                print("No pay found: " + jobTitle.text.strip() + " (" + companyName.text.strip() + ")")
                payText = "NA"
                
            finally:
                jobs_data.append((jobTitleText, companyNameText, payText, jobDescription, jobInfoText))
                    
        nextPageLinkLocator = (By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
        sleep_random(3, 4)
        
        jobsCounted += 1
        if jobsCounted % SAVE_INTERVAL == 0:
            write_to_csv()
        
        try:
            wait.until(EC.element_to_be_clickable(nextPageLinkLocator)).click()
            currentPage += 1
            
        except Exception as e:
            print(e)
            finalize()
            
except Exception as e:
    print(e)
            
finally:
    finalize()