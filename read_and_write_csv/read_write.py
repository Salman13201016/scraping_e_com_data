import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set Chrome options (if needed)
chrome_options = Options()
# Add any desired options to the chrome_options object

# Create the WebDriver instance
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.daraz.com.bd/"
driver.get(url)

# Find and click the "Electronic Accessories" category
category_element = driver.find_element(By.LINK_TEXT, "Electronic Accessories")
category_element.click()

# Define the range of subcategory elements you want to scrape
start_index = 1  # First element index
end_index = 10   # Last element index

subcategory_links = []
for i in range(start_index, end_index + 1):
    css_selector = f"#J_3442298940 > div > ul > ul.lzd-site-menu-sub.Level_1_Category_No8 > li:nth-child({i}) > a > span"
    #J_3442298940 > div > ul > ul.lzd-site-menu-sub.Level_1_Category_No8 > li:nth-child(1) > a > span
    subcategory_element = driver.find_element(By.CSS_SELECTOR, css_selector)
    subcategory_link = subcategory_element.find_element(By.XPATH, "..").get_attribute("href")
    subcategory_links.append(subcategory_link)

# Store the subcategory links in a CSV file
csv_file = "subcategory_links.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Subcategory Links"])
    writer.writerows([[link] for link in subcategory_links])

# Close the WebDriver instance
driver.quit()

# Now, read the links from the CSV file and open them one by one
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        link = row[0]
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(link)
        # Add your scraping code here for each subcategory page
        driver.quit()
