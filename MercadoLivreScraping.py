import requests
from bs4 import BeautifulSoup

class ScrapingML():
    def __init__(self, link):
        self.link = link
        self.soup = BeautifulSoup

    def request(self):
        page = requests.get(self.link)
        return BeautifulSoup(page.text, 'html.parser')

    def title(self, soup):
        return soup.find(class_="poly-component__title").text

    def amount_discount(self, soup):
        return soup.find(class_='andes-money-amount__discount').text

    def find_children(self, soup, children, text):
        if text:
            children_find = []
            for string in soup.find(class_='poly-component__price').children:
                children_find.append(string.find_next(class_=children).text)
            return children_find
        else:
            children_find = []
            for string in soup.find(class_='poly-component__price').children:
                children_find.append(string.find_next(class_=children))
            return children_find
