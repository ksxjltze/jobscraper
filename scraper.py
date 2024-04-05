from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://sg.indeed.com/jobs?q=software+engineer+entry+level&l=Singapore")


title = driver.title
jobs = driver.find_elements(By.CLASS_NAME, "tapItem")
wait = WebDriverWait(driver, 20)

acceptCookiesButtonLocator = (By.ID, "onetrust-accept-btn-handler")
wait.until(EC.element_to_be_clickable(acceptCookiesButtonLocator))
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

jobs_with_salary = []

for job in jobs:
    errors = [NoSuchElementException]
    
    wait.until(EC.element_to_be_clickable(job))
    job.click()
    
    try:
        jobPane = driver.find_element(By.ID, "jobsearch-ViewjobPaneWrapper")
    except:
        skeletonLocator = (By.XPATH, "//div[@data-testid='viewJob-skeleton']")
        wait.until(EC.presence_of_element_located(skeletonLocator))
        
    jobTitle = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "span")
    companyInfo = job.find_element(By.CLASS_NAME, "company_location")
    companyName = companyInfo.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
    
    try:
        element = driver.find_element(By.ID, "salaryInfoAndJobType")
        salaryInfo = element.text
        jobs_with_salary.append((jobTitle.text, companyName.text, salaryInfo))
    except:
        try:
            payElement = driver.find_element(By.XPATH, "//div[@aria-label='Pay']")
            payString = payElement.text
            jobs_with_salary.append((jobTitle.text, companyName.text, payString))
            
        except:
            print("No pay found for job: " + jobTitle.text + " (" + companyName.text + ")")
            
for job in jobs_with_salary:
    print(job[0] + "( " + job[1] + ")" + " - " + job[2])
        
driver.quit()