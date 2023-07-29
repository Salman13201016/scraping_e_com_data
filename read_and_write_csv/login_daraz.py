import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

print("Just a line added")

chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
# Remove the headless argument to show the Chrome browser window
# chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Start the service

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.daraz.com.bd/"
driver.get(url)

click_login = driver.find_element(By.CSS_SELECTOR, "#anonLogin > a").click()
time.sleep(5)
click_register = driver.find_element(By.XPATH, "//*[@id='container']/div/div[1]/div/span/a").click()
time.sleep(5)
phone_number = driver.find_element(By.XPATH, "//*[@id='container']/div/div[2]/form/div/div[1]/div[1]/input").send_keys('+8801742623564')
time.sleep(5)
full_name = driver.find_element(By.XPATH, "//*[@id='container']/div/div[2]/form/div/div[2]/div[1]/input").send_keys('Nirban Mitra')
time.sleep(5)
password = driver.find_element(By.XPATH, "//*[@id='container']/div/div[2]/form/div/div[1]/div[3]/input").send_keys('N@10203040')
time.sleep(5)

# Click on the birthday month dropdown
click_birthday_month = driver.find_element(By.XPATH, "//*[@id='month']/span/span").click()
time.sleep(2)

# Select February from the dropdown
select_birthday_month = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'February')]"))
).click()

click_birthday_day = driver.find_element(By.XPATH, "//*[@id='day']/span").click()
time.sleep(2)
select_birthday_day = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), '11')]"))
).click()

click_birthday_year = driver.find_element(By.XPATH, "//*[@id='year']/span/span").click()
time.sleep(2)
select_birthday_year = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), '1997')]"))
).click()

click_gender = driver.find_element(By.XPATH, "//*[@id='gender']/span/span").click()
time.sleep(2)
select_gender = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'male')]"))
).click()

click_signup = driver.find_element(By.XPATH, "//*[@id='container']/div/div[2]/form/div/div[2]/div[3]/button").click()

# Wait for a few seconds to see the result before closing the browser
time.sleep(10)

driver.quit()
