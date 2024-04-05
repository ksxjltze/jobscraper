from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)

options.add_argument(f'--user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

import time;
import random;

driver = webdriver.Chrome()
driver.get("https://sg.indeed.com/jobs?q=software+engineer+entry+level&l=Singapore")
driver.maximize_window()

title = driver.title
wait = WebDriverWait(driver, 60)

acceptCookiesButtonLocator = (By.ID, "onetrust-accept-btn-handler")
wait.until(EC.element_to_be_clickable(acceptCookiesButtonLocator)).click()

jobs_with_salary = []

def clamp(x, a, b):
    return max(a, min(x, b))

def sleep_random(min_sleep_time, max_sleep_time): 
    sleep_time = random.random() * max_sleep_time
    sleep_time_clamped = clamp(sleep_time, min_sleep_time, max_sleep_time)
    
    time.sleep(sleep_time_clamped)

while True:
    jobs = driver.find_elements(By.CLASS_NAME, "tapItem")
    for job in jobs:
        errors = [NoSuchElementException]
        
        wait.until(EC.element_to_be_clickable(job))
        job.click()
        
        sleep_random(2, 3)
        
        try:
            jobPane = driver.find_element(By.ID, "jobsearch-ViewjobPaneWrapper")
        except:
            skeletonLocator = (By.XPATH, "//div[@data-testid='viewJob-skeleton']")
            wait.until(EC.presence_of_element_located(skeletonLocator))
        
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jobsearch-JobInfoHeader-title")))
        
        jobTitle = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "span")
        companyInfo = job.find_element(By.CLASS_NAME, "company_location")
        companyName = companyInfo.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
        
        jobTitleText = jobTitle.text.strip()
        companyNameText = companyName.text.strip()
        
        try:
            payElement = driver.find_element(By.XPATH, "//div[@aria-label='Pay']")
            payText = payElement.text.strip().removeprefix("Pay\n")
            
            jobs_with_salary.append((jobTitleText, companyNameText, payText))
            print(payText + " (" + jobTitleText + ")" + " - " + companyNameText)
            
        except:
            print("No pay found for job: " + jobTitle.text.strip() + " (" + companyName.text.strip() + ")")
                
    nextPageLinkLocator = (By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
    sleep_random(2, 3)
    wait.until(EC.element_to_be_clickable(nextPageLinkLocator)).click()
                
    for job in jobs_with_salary:
        print(job[0] + " (" + job[1] + ")" + " - " + job[2])
        
driver.quit()