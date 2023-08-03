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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

# Set the path for the ChromeDriver
chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'

# Chrome options to run the browser in headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)
chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'


chrome_options = webdriver.ChromeOptions()
# Remove the headless argument to show the Chrome browser window
# chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)


url = "https://www.daraz.com.bd/"
driver.get(url)

# Find and click the "Electronic Accessories" category
category_element = driver.find_element(By.LINK_TEXT, "Electronic Accessories")
category_element.click()
# Define the range of subcategory elements you want to scrape
start_index = 1  # First element index
end_index = 10   # Last element index

subcategory_data = []  # List to store subcategory name and link as tuples

for i in range(start_index, end_index + 1):
    css_selector = f"#J_3442298940 > div > ul > ul.lzd-site-menu-sub.Level_1_Category_No8 > li:nth-child({i}) > a > span"
    subcategory_element = driver.find_element(By.CSS_SELECTOR, css_selector)
    subcategory_name = subcategory_element.text
    subcategory_link = subcategory_element.find_element(By.XPATH, "..").get_attribute("href")
    subcategory_data.append((subcategory_name, subcategory_link))

# Store the subcategory names and links in a CSV file
csv_file = "subcategory_links.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Subcategory Name", "Subcategory Link"])
    writer.writerows(subcategory_data)

# Function to collect product links from a single page
# ... (previous code)

# Function to collect product links from a single page
def collect_product_links():
    max_retries = 3  # Maximum number of retries before giving up
    retries = 0

    while retries < max_retries:
        try:
            grid_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gridItem--Yd0sa")))
            product_links = [item.find_element(By.CSS_SELECTOR, "a").get_attribute("href") for item in grid_items]
            return product_links
        except StaleElementReferenceException:
            # If a StaleElementReferenceException occurs, wait for a moment and try again
            retries += 1
            time.sleep(1)
            print(f"Retry attempt {retries} for collecting product links.")
    
    # If all retries failed, raise an exception
    raise Exception("Failed to collect product links after multiple retries.")


# Function to scroll down to the bottom of the page
# ... (Previous code)

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Adjust the wait time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to collect all product links from a subcategory page
def collect_all_product_links(subcategory_link, total_pages=102):
    driver.get(subcategory_link)
    time.sleep(3)

    all_product_links = []
    page_number = 1

    while page_number <= total_pages:
        try:
            print(f"Scraping page {page_number} from {subcategory_name}")
            product_links = collect_product_links()
            print(f"Found {len(product_links)} product links on this page")
            all_product_links.extend(product_links)

            # Scroll to the bottom of the page to load more products
            scroll_to_bottom()

            # Click the "Next" button using JavaScript click
            next_button = driver.find_element(By.XPATH, f"//a[text()='{page_number + 1}']")
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the next page to load (you can increase this time if needed)
            time.sleep(3)
            page_number += 1
        except (TimeoutException, NoSuchElementException):
            # No "Next" button found or reached the desired total_pages, exit the loop
            break

    return all_product_links

# ... (Remaining code)

    driver.get(subcategory_link)
    time.sleep(3)

    all_product_links = []
    page_number = 1

    while page_number <= total_pages:
        try:
            print(f"Scraping page {page_number}")
            product_links = collect_product_links()
            print(f"Found {len(product_links)} product links on this page")
            all_product_links.extend(product_links)

            # Click the "Next" button using JavaScript click
            next_button = driver.find_element(By.XPATH, f"//a[text()='{page_number + 1}']")
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the next page to load (you can increase this time if needed)
            time.sleep(3)
            page_number += 1
        except (TimeoutException, NoSuchElementException):
            # No "Next" button found or reached the desired total_pages, exit the loop
            break

    return all_product_links

    driver.get(subcategory_link)
    time.sleep(3)

    all_product_links = []
    page_number = 1

    while page_number <= total_pages:
        try:
            print(f"Scraping page {page_number}")
            product_links = collect_product_links()
            print(f"Found {len(product_links)} product links on this page")
            all_product_links.extend(product_links)

            # Click the "Next" button using JavaScript click
            next_button = driver.find_element(By.XPATH, f"//a[text()='{page_number + 1}']")
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the next page to load (you can increase this time if needed)
            time.sleep(3)
            page_number += 1
        except (TimeoutException, NoSuchElementException):
            # No "Next" button found or reached the desired total_pages, exit the loop
            break

    return all_product_links

# Read subcategory data from CSV
csv_file = "subcategory_links.csv"
subcategory_data = []
with open(csv_file, newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        subcategory_name, subcategory_link = row
        subcategory_data.append((subcategory_name, subcategory_link))

# Collect all product links from all subcategory pages and store them in separate CSV files
for subcategory_name, subcategory_link in subcategory_data:
    # Collect product links for each subcategory
    all_product_links = collect_all_product_links(subcategory_link)

    # Store all the product links in a separate CSV file with the subcategory name
    product_links_csv = f"{subcategory_name}_product_links.csv"
    with open(product_links_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Links"])
        writer.writerows([[link] for link in all_product_links])

# Close the WebDriver instance
driver.quit()
