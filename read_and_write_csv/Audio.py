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
from selenium.webdriver.common.action_chains import ActionChains
# ... (previous code)

from selenium.common.exceptions import NoSuchElementException

# ... (previous code)


# Set the path for the ChromeDriver
chrome_driver_path = r'H:\\STUDY\\Python Projects VSML\\webdriver\\chromedriver.exe'

# Chrome options to run the browser in headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

def collect_product_links():
    grid_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gridItem--Yd0sa")))
    product_links = [item.find_element(By.CSS_SELECTOR, "a").get_attribute("href") for item in grid_items]
    return product_links

def scrape_all_product_links(subcategory_link, total_pages=102):
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

            # Click the "Next" button
            next_button = driver.find_element(By.XPATH, f"//a[text()='{page_number + 1}']")
            actions = ActionChains(driver)
            actions.move_to_element(next_button).click().perform()

            # Wait for the next page to load (you can increase this time if needed)
            time.sleep(3)
            page_number += 1
        except (TimeoutException, NoSuchElementException):
            # No "Next" button found or reached the desired total_pages, exit the loop
            break

    return all_product_links

# Example: Open the "Audio" subcategory page
audio_subcategory_link = "https://www.daraz.com.bd/audio/"
all_audio_product_links = scrape_all_product_links(audio_subcategory_link)

# Store all the product links in a CSV file
audio_product_links_csv = "audio_product_links.csv"
with open(audio_product_links_csv, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Links"])
    writer.writerows([[link] for link in all_audio_product_links])

# Close the WebDriver instance
driver.quit()
