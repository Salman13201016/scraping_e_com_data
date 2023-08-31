import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException,ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import re, logging

def sanitize_filename(filename):
    sanitized_name = re.sub(r'[^\w\s-]', '', filename).strip()
    sanitized_name = re.sub(r'[-\s]+', '_', sanitized_name)
    return sanitized_name

def has_reviews(driver):
    try:
        review_element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[1]/div[3]/div[1]')
        return True
    except NoSuchElementException:
        return False

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger()

chrome_driver_path = r'C:\\Users\\nirba\\OneDrive\\Desktop\\Web Scrapping\\scrapping_product_details_from_daraz\\chromedriver-win64\\chromedriver.exe'

# Chrome options to run the browser in headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')

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

def is_next_button_disabled(driver):
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')
        return True
    except NoSuchElementException:
        return False

# Step 1: Read the saved links CSV file and scrape product details
with open("Audio_product_links.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        url = row[0]
        driver.get(url)
        logger.info(f'Scraping data from URL: {url}')

        # Wait for the page to load (you may need to adjust the waiting time)
        time.sleep(5)

        # Scrape product details using specific selectors for each detail
        try:
            title = driver.find_element(By.CSS_SELECTOR, '#module_product_title_1 > div > div > span').text
        except NoSuchElementException:
            title = 'Title not found'

        try:
            price = driver.find_element(By.CSS_SELECTOR, '#module_product_price_1 > div > div > div > span.pdp-price.pdp-price_type_deleted.pdp-price_color_lightgray.pdp-price_size_xs').text
        except NoSuchElementException:
            price = 'Price not found'

        try:
            discount_price = driver.find_element(By.CSS_SELECTOR, '#module_product_price_1 > div > div > span').text
        except NoSuchElementException:
            discount_price = 'Discount Price not found'

        try:
            rating = driver.find_element(By.CSS_SELECTOR, '#module_product_review_star_1 > div > div').text
        except NoSuchElementException:
            rating = 'Rating not found'

        try:
            description = driver.find_element(By.CSS_SELECTOR, '#module_product_detail').text
        except NoSuchElementException:
            description = 'Description not found'

        # Scroll down to the review section using JavaScript
        
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//*[@id="module_product_review"]'))

        # Locate the element you want to scroll into view
        review_section = driver.find_element(By.XPATH, '//*[@id="module_product_review"]')

        # Get the current scroll position
        current_scroll_position = driver.execute_script("return window.pageYOffset;")

        # Get the target scroll position (element's top position)
        target_scroll_position = review_section.location["y"]

        # Calculate the number of pixels to scroll in each step
        scroll_step = 10  # You can adjust this value to control the scrolling speed

        # Scroll towards the target position
        while current_scroll_position < target_scroll_position:
            # Calculate the new scroll position
            new_scroll_position = min(current_scroll_position + scroll_step, target_scroll_position)

            # Scroll to the new position using JavaScript
            driver.execute_script(f"window.scrollTo(0, {new_scroll_position});")

            # Update the current scroll position
            current_scroll_position = new_scroll_position

            # Add a short delay to control the scroll speed
            time.sleep(0.1)  # Adjust this value as needed

        # Scrape comments from all pages
        if has_reviews(driver):
            try:
                comments = []  # Initialize an empty list for comments
                while True:
                    try:
                        for i in range(1, 6):  # Loop from 1 to 5 to scrape all 5 reviews
                            comment_element_xpath = '//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[' + str(i) + ']/div[3]/div[1]'
                            try:
                                comment_element = driver.find_element(By.XPATH, comment_element_xpath)
                                comments.append(comment_element.text)
                            except StaleElementReferenceException:
                                # Handle stale element reference by re-locating the element
                                comment_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, comment_element_xpath)))
                                comments.append(comment_element.text)

                        # Check if there's a next page button
                        next_page_button = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')))
                        if not next_page_button:
                            break

                        # Click the next page button
                        if is_next_button_disabled(driver):
                            next_page_button = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]')))
                            if next_page_button.is_enabled():
                                try:
                                    next_page_button.click()
                                    time.sleep(5)
                                except ElementClickInterceptedException:
                                    break
                            else:
                                break
                        # Re-locate elements after the page refresh
                        else:
                            logger.info("No Next Button")
                    except NoSuchElementException:
                        comments.append('Comments not found')
            except NoSuchElementException:
                comments.append('Comments not found')
            except TimeoutException:
                comments.append('Timed out waiting for the "Next" button')
        else:
            comments = ['No reviews available']

        # Prepare the data to be written to the CSV
        product_data = [[title, url, price, discount_price, rating, description, '\n'.join(comments)]]

        # Generate the CSV file name based on the product title
        csv_file_name = f"{sanitize_filename(title)}.csv"

        # Write the data to the CSV file
        write_to_csv(csv_file_name, product_data)
        logger.info(f'Data scraped and saved to {csv_file_name}')

# Quit the driver
driver.quit()
