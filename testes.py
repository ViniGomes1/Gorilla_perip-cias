import requests
from bs4 import BeautifulSoup

#sem pix https://mercadolivre.com/sec/2zFh8Qs
#com pix https://mercadolivre.com/sec/2WXZqrh

#SEM PROMOCAO https://mercadolivre.com/sec/1SQ9LGG
#COM PROMOCAO https://mercadolivre.com/sec/1pwcgie

link = "https://mercadolivre.com/sec/1SQ9LGG"

page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')

parent_component = soup.find("div", class_="poly-component__price")

children_find = []
amount = None
product_final = ""
discount = []

for string in soup.find(class_='poly-component__price').children:
    children_find.append(string.find_next(class_="andes-money-amount__fraction").text)
    amount = soup.find(class_='andes-money-amount__discount').text

for string in soup.find(class_='poly-component__price').children:
    discount.append(string.find_next(class_="poly-price__installments"))

product_title = soup.find(class_="poly-component__title").text
amount_discount = soup.find(class_='andes-money-amount__discount').text



if len(children_find) <= 2:
    product_final = link + """

""" + product_title + """

POR: """ + children_find[0] + """
""" + discount[0].text

else:
    product_final = link + """
    

""" + product_title + """

DE: """ + children_find[0] + """
Por: """ + children_find[1] + """
""" + discount[0].text

print(product_final)

'''
for child in parent_component.find_all(recursive=False):
    children_find.append(child.find_next(class_="andes-money-amount__fraction").text)
    if 'andes-money-amount--previous' in child.get('class', []):
        print("encontrado")
    else:
        print("not found")
'''

#print(children_find, amount)
