from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

class ScrapingAmazon():
    def __init__(self, link):
        self.link = link
        self.soup = BeautifulSoup

    def discountVerify(self, core_price):
        percentage = core_price.find(core_price.find(class_="savingsPercentage"))
        if percentage is not None:
            return False
        else:
            return True

    def percentageDiscount(self, core_price):
        return core_price.find(class_="savingsPercentage").text


    def discountPrice(self, core_price):
        discount_price = []

        discount_price_find = core_price.find(class_="basisPrice")
        for children in discount_price_find.find(class_="a-price"):
            discount_price.append(children.text)

        return discount_price

    def totalPrice(self, core_price):
        parent = core_price.find(class_="priceToPay")
        total_price = []
        for index, child in enumerate(parent.find_all(recursive=False)):
            if index < 2:
                total_price.append(child.text)
            else:
                break
        return total_price

    def title(self, soup):
        return soup.find(id="productTitle").text

    def corePrice(self, soup):
        soup.find(id="corePriceDisplay_desktop_feature_div")
        return soup
    def image_source(self, soup):
        return soup.find(class_="a-dynamic-image")['src']

    def requestSelenium(self):

        edgeOptions = Options()

        edgeOptions.add_argument("--headless=new")
        edgeOptions.add_argument('--disable-gpu')
        edgeOptions.add_argument('--no-sandbox')
        edgeOptions.add_argument('--disable-dev-shm-usage')
        edgeOptions.add_argument("--disable-javascript")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=edgeOptions)

        try:
            driver.get(self.link)
            html = driver.page_source
            return BeautifulSoup(html, 'html.parser')
        except TimeoutException:
            return "Não deu"
        finally:
            driver.delete_all_cookies()
            driver.quit()