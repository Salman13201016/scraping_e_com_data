import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Set up the ChromeDriver service
service = Service(ChromeDriverManager().install())

# Set Chrome options (if needed)
chrome_options = webdriver.ChromeOptions()
# Add any desired options to the chrome_options object

# Create the WebDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Daraz website
url = "https://www.daraz.com.bd/"
driver.get(url)

# Define the range of main categories
first_main_category = 1
last_main_category = 12

# Create the "Main Categories" folder
main_categories_folder = "Main Categories"
os.makedirs(main_categories_folder, exist_ok=True)

# Loop through each main category in ascending order
for i in range(first_main_category, last_main_category + 1):
    # Construct the CSS selector dynamically for main category
    main_category_selector = f"#Level_1_Category_No{i} > a > span"
    
    # Find the main category element
    main_category_element = driver.find_element(By.CSS_SELECTOR, main_category_selector)
    
    # Get the main category name
    main_category_name = main_category_element.text
    
    # Create a folder for the main category
    main_category_folder = os.path.join(main_categories_folder, main_category_name)
    os.makedirs(main_category_folder, exist_ok=True)
    
    # Click on the main category to reveal the subcategories
    main_category_element.click()
    
    # Wait for the subcategory elements to be visible
    subcategory_selector = f"#J_3442298940 > div > ul > ul.lzd-site-menu-sub.Level_1_Category_No1 > li:nth-child({i}) > a > span"
    subcategory_elements = driver.find_elements(By.CSS_SELECTOR, subcategory_selector)
    
    # Store the subcategories inside the main category folder
    for subcategory_element in subcategory_elements:
        subcategory_name = subcategory_element.text
        subcategory_folder = os.path.join(main_category_folder, subcategory_name)
        os.makedirs(subcategory_folder, exist_ok=True)

# Close the browser
driver.quit()
