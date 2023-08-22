import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys



service = Service(ChromeDriverManager().install())

# Set Chrome options (if needed)
chrome_options = webdriver.ChromeOptions()
# Add any desired options to the chrome_options object

# Create the WebDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Facebook's Ostad page
driver.get("https://www.facebook.com/ostadapp/reviews")

# Wait for the page to load
time.sleep(10)

# Find the "Log In" button and click it


# Wait for the login form to appear
time.sleep(10)

# Enter your email/phone and password and press Enter
email_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "email"))
)
email_input.send_keys("nirbanmitra007@gmail.com")
time.sleep(10)
password_input = driver.find_element(By.XPATH, '//*[@id="pass"]')
password_input.send_keys("Nirban@007")
time.sleep(10)


# Find the "Reviews" link within the navigation bar and click it
# reviews_link = nav_bar.find_element(By.PARTIAL_LINK_TEXT, "Reviews")
# reviews_link.click()
# review_page_link.click()
# # Wait for the login to complete (you can adjust the waiting time)

# wait = WebDriverWait(driver, 10)

# # Find and click the "Reviews" link
# reviews_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Reviews")))
# reviews_link.click()

# Wait for the review page to load


# Scroll down to load more reviews (you can repeat this as needed)
scroll_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")
    if new_scroll_height == scroll_height:
        break
    scroll_height = new_scroll_height

# At this point, you should be on the review page with loaded reviews.

# You can now extract the reviews as needed.

# Finally, close the browser when done.
driver.quit()
