import os
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from tqdm import tqdm







URL = "https://www.ebay.com/b/Toys-Hobbies/220/bn_1865497"
DATA_PATH = "Data"

brands = []
products = []
conditions = []
prices = []
available_qnts = []
sold_qnts = []

# driver = webdriver.Chrome()
# driver.get("https://www.ebay.com/itm/176877126325?itmmeta=01JV2XDEVHVW1N7ATPMPH5ENEM&hash=item292eb2c2b5:g:3d8AAOSwyhZoCRo~&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kOdIQ7cPuoSCb9137zGcW7bkBvHocjY4rhLtmkyd37WTw0lkGxAtAwwnCb%2FG0WXPH9okuRQhBvl%2F1UgSmFFA7kUBctH0s90zrEwXBB%2B%2B8ErWn6dFBfT6VuBvAoUt927CBQ5CnpTrmrDfyw7FobgIixI1fuxbmJGiWFvVct6ozJvAIMWfoCAAcQDTClf73I38qh9quuj%2BLMCZRton7P%2F1%2Brc8usgd%2B%2FBM0GveE4i%2FcOivgRWgLj6PwUnKpeHrjOPHHhyZMNdOumj7YygubIRYbT%7Ctkp%3ABFBM9O213dhl")

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('disable-notifications')

chrome_options.add_argument("window-size=1280,720")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL) 

i= 0

while True:
    links = driver.find_elements(By.CSS_SELECTOR, "section.brw-river a.bsig__title__wrapper")
    product_urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    for url in product_urls:
        # Open in a new tab
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
        time.sleep(2) 
        # extracting each product info
        try:
            brand = driver.find_element(By.CSS_SELECTOR, "div.x-sellercard-atf__info__about-seller span.ux-textspans.ux-textspans--BOLD").text
            product = driver.find_element(By.CSS_SELECTOR, "h1.x-item-title__mainTitle span").text
            condition = driver.find_element(By.CSS_SELECTOR, "div.x-item-condition-text span.ux-textspans").text
            price = driver.find_element(By.CSS_SELECTOR, "div.x-bin-price__content span").text
            available_qnt = driver.find_element(By.CSS_SELECTOR, "div.x-quantity__availability span:nth-of-type(1)").text
            sold_qnt = driver.find_element(By.CSS_SELECTOR, "div.x-quantity__availability span:nth-of-type(2)").text

            # keep data
            brands.append(brand)
            products.append(product)
            conditions.append(condition)
            prices.append(price)
            available_qnts.append(available_qnt)
            sold_qnts.append(sold_qnt)

  
 
        except Exception as e:
            print("Error Scraping", e)
        
        # Back to the main page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    # Go to next Page:
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination__next")
        next_button.click()
        print('Next Page')
        i +=1
        
        time.sleep(3)
    except:
        print('No More Pages.')
        break

    if i == 15:
        break

driver.quit()

df= pd.DataFrame({'toy': products, 'brand': brands, 'condition': conditions, 'price': prices,
                              'available_quantity': available_qnts, 'sold_quantity': sold_qnts})
df.to_csv(os.path.join(DATA_PATH, 'toys_data.csv'), index= False)


print('Saved!')


