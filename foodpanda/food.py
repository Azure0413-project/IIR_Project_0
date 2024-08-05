import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# change the url you want to get
# if catch item occur error, please change the pauseTimem and srollHeight below. roll_web(Line:48). smaller is recommanded. 
url = "https://www.foodpanda.com.tw/restaurant/a9is/jia-andb-coffee-takeaway-bar-tai-nan-guang-ming-dian"
# you need to change id every round
id = 0



def roll_web(driver, pauseTime = 1, srollHeight = 300, final_stop = 2):
    SCROLL_PAUSE_TIME = pauseTime

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    now_height = 0

    while now_height < last_height:
        # Scroll down to bottom
        driver.execute_script("window.scrollBy(0, " + str(srollHeight) + ");")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        now_height += srollHeight
    
    time.sleep(final_stop)


def crawler(url, id):
    # web address (TaiwanGoodInfo)
    
    # pretent it from the normal user
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

    # get the website
    driver = webdriver.Chrome()
    driver.get(url)

    # wait until element 
    _ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lazy-loaded-dish-photo")))
    roll_web(driver, pauseTime = 1, srollHeight = 300, final_stop = 5)


    # analyze the web
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # get the vendor name
    vendor = soup.find("h1", class_="sm:f-title-medium-font-size md:f-title-medium-font-size lg:f-title-medium-font-size xl:f-title-large-font-size f-title-xlarge-font-size sm:fw-title-medium-font-weight md:fw-title-medium-font-weight lg:fw-title-medium-font-weight xl:fw-title-large-font-weight fw-title-xlarge-font-weight sm:lh-title-medium-line-height md:lh-title-medium-line-height lg:lh-title-medium-line-height xl:lh-title-large-line-height lh-title-xlarge-line-height sm:ff-title-medium-font-family md:ff-title-medium-font-family lg:ff-title-medium-font-family xl:ff-title-large-font-family ff-title-xlarge-font-family sm:ffs-title-medium-font-feature-settings md:ffs-title-medium-font-feature-settings lg:ffs-title-medium-font-feature-settings xl:ffs-title-large-font-feature-settings ffs-title-xlarge-font-feature-settings")
    data_dir = os.path.join(os.getcwd(),"data")
    
    # create the folder
    vendor_dir = os.path.join(data_dir,vendor.text)
    os.makedirs(vendor_dir, exist_ok = True)

    # write into csv
    csv_path = os.path.join(vendor_dir, "vendor.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['id', 'vendor', 'product_name', 'product_price', 'product_img'])


    # get the product
    product_grid = soup.find_all("li", class_="box-flex product-tile fd-row p-relative pa-st")


    for grid in product_grid:

        name = grid.find("span", class_="vertical-align-middle")
        price = grid.find("p", class_="cl-neutral-primary f-paragraph-medium-font-size fw-paragraph-medium-font-weight lh-paragraph-medium-line-height ff-paragraph-medium-font-family")
        price = price.text[price.text.find('$')+1:]
        # print(pic["style"].split("\"")[1])
        # download the pic
        pic = grid.find("div", class_="lazy-loaded-dish-photo")
        pic_url = pic["style"].split("\"")[1]
        if(pic["style"] != None):
            pic_path = os.path.join(vendor_dir, str(id) + ".jpeg")
            with open(pic_path, "wb") as f:
                f.write(requests.get(pic_url).content)

        
        # write into csv
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 寫入一列資料
            writer.writerow([str(id), vendor.text, name.text, price, pic_url])
        id += 1
    
    print(f"Id for next Round is: {id}")


crawler(url, id)