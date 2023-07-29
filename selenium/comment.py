# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# import time
# import requests

# driver = webdriver.Chrome(ChromeDriverManager().install())

# driver.maximize_window()
# driver.get("https://www.daraz.com.bd/products/attar-al-kaaba-by-al-haaramain-made-in-saudi-arabia-premium-arabian-attar-3ml-6ml-12ml-i306519311-s1382129894.html")


# comment_list = []

# h = driver.execute_script('return document.body.scrollHeight')

# for p in range(0,h+1000,30):
#     driver.execute_script(f'window.scrollTo(0,{p});')
#     time.sleep(0.2)

# all_comments = driver.find_elements(By.CLASS_NAME,'content')

# for i in all_comments:
#     comment_list.append(i.text)
    
# print(comment_list)

# # print(title_list,"/n",link_list,"/n",image_list)

# # print(len(title_list),"/n",len(link_list),"/n",len(image_list))

# # response = requests.get(prod_image)

# # with open("1.jpg", "wb") as file:
# #     file.write(response.content)
# # driver.get(prod_link)
# import pandas as pd

# data = {"Comment":comment_list}
# df = pd.DataFrame(data)
# df.to_csv('output1.csv', index=False)

# time.sleep(40)


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.comon.by import By
# from selenium.webdriver.comon.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import time



driver = webdriver.Chrome(ChromeDriverManager().install())

print("line added")

driver.get("https://www.daraz.com.bd/groceries-laundry-household-laundry-washing-liquid/")

time.sleep(10)