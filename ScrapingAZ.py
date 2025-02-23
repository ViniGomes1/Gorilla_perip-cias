from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import time
from bs4 import BeautifulSoup, PageElement

start = time.time()

edgeOptions = Options()
edgeOptions.add_argument("--headless=new")
edgeOptions.add_argument('--disable-gpu')
edgeOptions.add_argument('--no-sandbox')
edgeOptions.add_argument('--disable-dev-shm-usage')
edgeOptions.add_argument("--disable-javascript")
driver = webdriver.Chrome(options=edgeOptions, service=Service(ChromeDriverManager().install()))
soup = BeautifulSoup

#promo https://amzn.to/3CQc1EO
#sem promo https://amzn.to/4jfyjAh

try:
    driver.get("https://amzn.to/4jfyjAh")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
except TimeoutException:
    print("Deu")
finally:
    driver.delete_all_cookies()
    driver.quit()

core_price = soup.find(id="corePriceDisplay_desktop_feature_div")
percentage_discount = core_price.find(class_="savingsPercentage")

parent = core_price.find(class_="priceToPay")
discount_price_find = core_price.find(class_="basisPrice")
product_titulo = soup.find(id="productTitle")

total_price = []
discount_price = []

for index, child in enumerate(parent.find_all(recursive=False)):
    if index < 2:
        total_price.append(child.text)
    else:
        break

if percentage_discount is not None:
    for children in discount_price_find.find(class_="a-price"):
        discount_price.append(children.text)

final_text = ""

if percentage_discount is not None:
    final_text = product_titulo.text + """

DE: """ + discount_price[0] + """
PARA: """ + total_price[1] + " " + percentage_discount.text + "OFF"

else:
    final_text = product_titulo.text + """

POR APENAS: """ + total_price[1]

print(final_text)

end = time.time()
duration = end - start
print("Time: {} seconds".format(round(duration, 3)))
