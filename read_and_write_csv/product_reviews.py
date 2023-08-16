import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import re

def sanitize_filename(filename):
    sanitized_name = re.sub(r'[^\w\s-]', '', filename).strip()
    sanitized_name = re.sub(r'[-\s]+', '_', sanitized_name)
    return sanitized_name

# Set the path for the ChromeDriver
chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'

# Chrome options to run the browser in headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.maximize_window()

def write_to_csv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Price', 'Discount Price', 'Rating', 'Description', 'Comments'])
        writer.writerows(data)

# Step 1: Read the saved links CSV file and scrape product details
with open("Audio_product_links.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        url = row[0]
        driver.get(url)

        # Wait for the page to load (you may need to adjust the waiting time)
        time.sleep(5)

        # Scrape product details using specific selectors for each detail
        try:
            title = driver.find_element(By.CSS_SELECTOR,'#module_product_title_1 > div > div > span').text
        except NoSuchElementException:
            title = 'Title not found'

        try:
            price = driver.find_element(By.CSS_SELECTOR,'#module_product_price_1 > div > div > div > span.pdp-price.pdp-price_type_deleted.pdp-price_color_lightgray.pdp-price_size_xs').text
        except NoSuchElementException:
            price = 'Price not found'

        try:
            discount_price = driver.find_element(By.CSS_SELECTOR,'#module_product_price_1 > div > div > span').text
        except NoSuchElementException:
            discount_price = 'Discount Price not found'

        try:
            rating = driver.find_element(By.CSS_SELECTOR,'#module_product_review_star_1 > div > div').text
        except NoSuchElementException:
            rating = 'Rating not found'

        try:
            description = driver.find_element(By.CSS_SELECTOR,'#module_product_detail').text
        except NoSuchElementException:
            description = 'Description not found'

        # Scrape comments using the provided selectors
        comments = []
        try:
            comment_elements = driver.find_elements(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[1]/div[3]/div[1]')
            for comment_element in comment_elements:
                comments.append(comment_element.text)
        except NoSuchElementException:
            comments.append('Comment not found')

        # Prepare the data to be written to the CSV
        product_data = [[title, url, price, discount_price, rating, description, '\n'.join(comments)]]

        # Generate the CSV file name based on the product title
        csv_file_name = f"{sanitize_filename(title)}.csv"

        # Write the data to the CSV file
        write_to_csv(csv_file_name, product_data)

driver.quit()

