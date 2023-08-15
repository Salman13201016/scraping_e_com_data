import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import csv

chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

product_url = "https://www.daraz.com.bd/products/pc-baseus-usb-50-i312318610-s1407208392.html?spm=a2a0e.searchlist.list.1.7330174fbOQAdj&search=1"
driver.get(product_url)

# Scroll down to the review section
review_section = driver.find_element(By.XPATH, '//*[@id="module_product_qna"]')
driver.execute_script("arguments[0].scrollIntoView();", review_section)

# Wait for a moment to ensure the content is loaded
driver.implicitly_wait(5)

# Selector for the review elements
review_selector = '//*[@id="module_product_qna"]/div/div[2]/div[2]/ul/li/div[1]/div[1]'

# Collect and store the reviews
reviews = []

while True:
    try:
        review_elements = driver.find_elements(By.XPATH, review_selector)
        for review_element in review_elements:
            review_text = review_element.text
            reviews.append(review_text)
        
        next_button = driver.find_element(By.XPATH, '//*[@id="module_product_qna"]/div/div[2]/div[2]/div[2]/div/button[2]')
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("window.scrollBy(0, -100);")  # Scroll a bit more to avoid overlapping elements
        next_button.click()
        time.sleep(2)  # Adjust this wait time as needed
        
        # last_page_class = '//*[@id="module_product_qna"]/div/div[2]/div[2]/ul'
        # last_page_button = driver.find_element(By.XPATH, f'//*[@class="{last_page_class}"]')
        # if "next-disabled" in last_page_button.get_attribute("class"):
        #     break
    except NoSuchElementException:
        break

# Store the collected reviews in a CSV file
csv_file = 'product_reviews.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Review'])
    writer.writerows([[review] for review in reviews])

# Close the WebDriver
driver.quit()
