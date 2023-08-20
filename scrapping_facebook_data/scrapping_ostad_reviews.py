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

service = Service(ChromeDriverManager().install())

# Set Chrome options (if needed)
chrome_options = webdriver.ChromeOptions()
# Add any desired options to the chrome_options object

# Create the WebDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.facebook.com/ostadapp?mibextid=ZbWKwL"
driver.get(url)
time.sleep(15)
# exit_login = driver.find_element(By.XPATH, '//*[@id="mount_0_0_Yg"]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div').click()
email_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form"]/div[2]/div[1]/label/input'))
)
time.sleep(15)
# Once the element is clickable, you can interact with it
email_input.send_keys('nirbanmitra007@gmail.com')
# email_input = WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="login_form"]/div[2]/div[1]/label/input'))
# )
# email_input.send_keys('nirbanmitra007@gmail.com')
time.sleep(5)
# login_email = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[2]/div[1]/label/input').send_keys('nirbanmitra007@gmail.com')
login_password = driver.find_element(By.CSS_SELECTOR, '#login_form > div.x9f619.x1n2onr6.x1ja2u2z.x2lah0s.x13a6bvl.x6s0dn4.xozqiw3.x1q0g3np.x1pi30zi.x1swvt13.xexx8yu.xcud41i.x139jcc6.x4cne27.xifccgj.x1s85apg.x3holdf > div:nth-child(2) > label > input').send_keys('Nirban@007')
time.sleep(5)
login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form"]/div[2]/div[3]/div/div/div[1]'))
)

# Click the login button
login_button.click()


time.sleep(10)
# login_button = driver.find_element(By.CSS_SELECTOR, '#login_form > div.x9f619.x1n2onr6.x1ja2u2z.x2lah0s.x13a6bvl.x6s0dn4.xozqiw3.x1q0g3np.x1pi30zi.x1swvt13.xexx8yu.xcud41i.x139jcc6.x4cne27.xifccgj.x1s85apg.x3holdf > div:nth-child(3) > div > div > div.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x1ey2m1c.xds687c.xg01cxk.x47corl.x10l6tqk.x17qophe.x13vifvy.x1ebt8du.x19991ni.x1dhq9h.x1wpzbip').click()


# Find and click the "Electronic Accessories" category
# WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.XPATH, "//body[@class='fbIndex UIPage_LoggedOut _-kb _605a b_c3pyn-ahh x1 locale_en_GB']"))
# )
# review_element = WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_d9"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]')) and
#     EC.visibility_of_element_located((By.XPATH, '//*[@id="mount_0_0_d9"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]/div[1]'))
# )
# review_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, '//*[@id="mount_0_0_d9"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]/div[1]'))
# )
# review_element = driver.find_element(By.XPATH, '//*[@id="mount_0_0_/j"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]')
# review_element.click()

# review_bar = WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_8e"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div'))
    
# )

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="element_that_indicates_page_has_loaded"]'))
)

# Now, proceed to click the review page link
review_page_link = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_/j"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]/div'))
)
review_page_link.click()

# review_page = driver.find_element(By.XPATH, '//*[@id="mount_0_0_/j"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[4]/div/span')
# review_page.click()
time.sleep(10)
scroll_pause_time = 2
scroll_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")

    if new_scroll_height == scroll_height:
        break

    scroll_height = new_scroll_height

# Collect reviews
reviews = []

while True:
    try:
        # Find all review elements on the current page
        review_elements = driver.find_elements(By.XPATH, '//*[@id="mount_0_0_/j"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[3]/div')

        # Collect review text
        for review_element in review_elements:
            review_text = review_element.text
            reviews.append([review_text])

        # Scroll down to load more reviews
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for the new reviews to load

    except StaleElementReferenceException:
        # Handle stale element exception, if it occurs
        pass

    # Check if there are no more reviews to load (no new review elements)
    if len(review_elements) == len(reviews):
        break

# Create a CSV file and write the reviews
csv_filename = "facebook_reviews.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Review'])

    for review in reviews:
        csv_writer.writerow(review)

# Close the WebDriver
driver.quit()