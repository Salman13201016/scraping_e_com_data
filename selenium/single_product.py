from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()



title_list = []
link_list = []
image_list = []
for page in range(1,5):
    driver.get("https://www.daraz.com.bd/men-muslimin-shirts/?page="+str(page))

    for p in range(1,41):
        k = str(p)
        prod_title = driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/div['+k+']/div/div/div[2]/div[2]/a').text

        prod_link = driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/div['+k+']/div/div/div[2]/div[2]/a').get_attribute('href')

        prod_link = driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/div['+k+']/div/div/div[1]/div[1]/a/img').get_attribute('src')

        title_list.append(prod_title)
        link_list.append(prod_link)
        image_list.append(prod_link)


print(title_list,"/n",link_list,"/n",image_list)

print(len(title_list),"/n",len(link_list),"/n",len(image_list))

# response = requests.get(prod_image)

# with open("1.jpg", "wb") as file:
#     file.write(response.content)
# driver.get(prod_link)
import pandas as pd

data = {"Title":title_list, "Image Link":link_list,"image":image_list}
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)

time.sleep(40)