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

chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'


chrome_options = webdriver.ChromeOptions()
# Remove the headless argument to show the Chrome browser window
# chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Start the service

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)


# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

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

def scrape_all_product_links(subcategory_link):
    driver.get(subcategory_link)
    time.sleep(3)

    all_product_links = []
    page_number = 1
    while True:
        try:
            print(f"Scraping page {page_number}")
            product_links = collect_product_links()
            print(f"Found {len(product_links)} product links on this page")
            all_product_links.extend(product_links)

            # Check for the presence of the "Next" button and click it
            next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Next")))
            next_button.click()

            # Wait for the next page to load (you can increase this time if needed)
            time.sleep(3)
            page_number += 1
        except TimeoutException:
            # No "Next" button found, exit the loop
            break

    return all_product_links

def collect_product_links():
    # Wait for the grid items to be present (increase the wait time if needed)
    grid_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gridItem--Yd0sa")))

    # Collect the product links from each grid item
    product_links = [item.find_element(By.CSS_SELECTOR, "a").get_attribute("href") for item in grid_items]
    return product_links


# Collect all product links from all subcategory pages and store them in separate CSV files
for i, (subcategory_name, subcategory_link) in enumerate(subcategory_data):
    # Collect product links for each subcategory
    all_product_links = scrape_all_product_links(subcategory_link)

    # Store all the product links in a separate CSV file with the subcategory name
    product_links_csv = f"{subcategory_name}_product_links.csv"
    with open(product_links_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Links"])
        writer.writerows([[link] for link in all_product_links])

# Close the WebDriver instance
driver.quit()
