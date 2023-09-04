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
import re, logging, uuid, os

def sanitize_filename(filename):
    sanitized_name = re.sub(r'[^\w\s-]', '', filename).strip()
    sanitized_name = re.sub(r'[-\s]+', '', sanitized_name)
    return sanitized_name

MAX_FILENAME_LENGTH = 500
output_directory = r'C:\\Users\\nirba\\OneDrive\\Desktop\\scraping_ecom_product_details'


def generate_unique_filename(title):
    # Maximum allowed length for a filename (adjust as needed)
    max_filename_length = 50
    
    # Sanitize and abbreviate the title (limit to max_filename_length characters)
    sanitized_title = sanitize_filename(title)[:max_filename_length]
    
    # Append a timestamp to make the filename unique
    timestamp = time.strftime("%Y%m%d%H%M%S")
    csv_file_name = f"{sanitized_title}_{timestamp}.csv"
    
    # Generate the full file path by joining it with the output directory
    csv_file_path = os.path.join(output_directory, csv_file_name)
    
    # Check if the file already exists, and if so, add a numeric suffix
    count = 1
    while os.path.exists(csv_file_path):
        # If the filename is still too long, add a unique identifier
        if max_filename_length - len(timestamp) < 3:
            unique_id = str(uuid.uuid4())[:8]
            csv_file_name = f"{sanitized_title[:10]}_{unique_id}_{timestamp}.csv"
        else:
            csv_file_name = f"{sanitized_title[:max_filename_length - len(timestamp) - 1]}_{timestamp}.csv"
        
        csv_file_path = os.path.join(output_directory, csv_file_name)
        count += 1
    
    return csv_file_name

    # Sanitize and abbreviate the title (limit to 100 characters)
    sanitized_title = sanitize_filename(title)[:500]
    print(f"Sanitized Title: {sanitized_title}")  # Debug print
    
    # Append a timestamp to make the filename unique
    timestamp = time.strftime("%Y%m%d%H%M%S")
    csv_file_name = f"{sanitized_title}_{timestamp}.csv"
    print(f"CSV Filename: {csv_file_name}")  # Debug print
    
    # Generate the full file path by joining it with the output directory
    csv_file_path = os.path.join(output_directory, csv_file_name)
    
    # Check if the file already exists, and if so, add a numeric suffix
    count = 1
    while os.path.exists(csv_file_path):
        csv_file_name = f"{sanitized_title}_{timestamp}_{count}.csv"
        csv_file_path = os.path.join(output_directory, csv_file_name)
        count += 1
    
    return csv_file_name



def has_reviews(driver):
    try:
        review_element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[1]/div[3]/div[1]')
        return True
    except NoSuchElementException:
        return False

output_directory = r'C:\\Users\\nirba\\OneDrive\\Desktop\\scraping_ecom_product_details'

if not os.path.exists(output_directory):
    os.makedirs(output_directory, exist_ok=True)

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger()

chrome_driver_path = r'C:\\Users\\nirba\\OneDrive\\Desktop\\scraping_ecom_product_details\\chromedriver.exe'

# Chrome options to run the browser in headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')

# Create a Service object for the ChromeDriver
service = Service(chrome_driver_path)

# Create the WebDriver with the Service and ChromeOptions
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.maximize_window()

def load_url_with_retry(driver, url, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        try:
            driver.get(url)
            return  # If successful, exit the loop
        except TimeoutException:
            # Handle the timeout (e.g., log an error message)
            logger.warning(f"Timeout loading URL: {url}. Retrying ({retry_count + 1}/{max_retries})...")
            retry_count += 1

    # Handle the case where all retries failed
    logger.error(f"All retries failed for URL: {url}")
    # You can raise an exception or handle it as needed

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
with open("Computer Accessories_product_links.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        url = row[0]
        load_url_with_retry(driver, url)  # Retry loading the URL if a timeout occurs
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
        
        try:
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
        except NoSuchElementException:
            logger.warning("Review section not found on this page. Skipping reviews.")
        if has_reviews(driver):
            try:
                comments = []  # Initialize an empty list for comments
                while True:
                    try:
                        review_elements = driver.find_elements(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[1]/div')
                        for i in range(1, len(review_elements) + 1): # Loop from 1 to 5 to scrape all 5 reviews
                            comment_element_xpath = f'//*[@id="module_product_review"]/div/div/div[3]/div[1]/div[{i}]/div[3]/div[1]'
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
        csv_file_path = os.path.join(output_directory, csv_file_name)

        # Write the data to the CSV file
        write_to_csv(csv_file_name, product_data)
        logger.info(f'Data scraped and saved to {csv_file_name}')

# Quit the driver
driver.quit()
