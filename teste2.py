import requests
from bs4 import BeautifulSoup

from requests_html import HTMLSession



#https://amzn.to/3CQc1EO promo
link = "https://amzn.to/4jfyjAh"

session = HTMLSession()
response = session.get(link)

print(response.html.html)