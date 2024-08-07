import requests
import numpy as np
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# web address (TaiwanGoodInfo)
url = "https://www.foodpanda.com.tw/city/tainan-city"
# url = "https://www.foodpanda.com.tw/restaurant/a9is/jia-andb-coffee-takeaway-bar-tai-nan-guang-ming-dian"
# pretent it from the normal user
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

# get the website
response = requests.get(url, headers= headers)
response.encoding = "utf-8"

driver = webdriver.Chrome()
driver.get(url)
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lazy-loaded-dish-photo")))
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-image-wrapper")))

time.sleep(20)
soup = BeautifulSoup(driver.page_source, 'html.parser')


# analyze the web



# get the information (observe the info you) Ex: <tr id="row0">

# get the tittle
title = []
product_grid = soup.find_all("div", class_="tile-image-wrapper")

# product_grid = soup.find_all("li", class_="box-flex product-tile fd-row p-relative pa-st")
# product_name = soup.find_all("span", class_="vertical-align-middle")
# product_pic = soup.find_all("div", class_="lazy-loaded-dish-photo")
for c in product_grid:
    # print(c)
    title.append(c)
    # find the nearest text in this object

print(title[0])


# # get row
# table = []
# counter = 0
# row = soup.find("tr", id="row" + str(counter))
# while row:
#     row = row.find_all("td")
#     value = []
#     # get the text from row
#     for r in row:
#         if r.text is not None:
#             value.append(r.text)
#         else:
#             value.append(None)

#     # add into the table
#     table.append(value)
#     counter += 1
#     row = soup.find("tr", id="row" + str(counter))


# # write into csv
# with open('stockTable.csv', 'w', newline = '') as f:
#     writer = csv.writer(f, delimiter = ',')
#     writer.writerow(title)
#     for r in table:
#         writer.writerow(r)




