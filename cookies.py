#amazon testes

from AmazonScraping import ScrapingAmazon

#promo https://amzn.to/3CQc1EO
#sem promo https://amzn.to/4jfyjAh

link = "https://amzn.to/4jfyjAh"

scraping = ScrapingAmazon(link=link)


#elementos centrais
soup = scraping.requestSelenium()
core_price = scraping.corePrice(soup)

#elementos secundários
total_price = scraping.totalPrice(core_price)

discount_verify = scraping.discountVerify(core_price)

discount_price = []
percentage_discount = ""

image_source = scraping.image_source(soup)

if discount_verify:
    discount_price = scraping.discountPrice(core_price)
    percentage_discount = scraping.percentageDiscount(core_price)

titulo = scraping.title(soup)

final_text = ""


if discount_verify:
    final_text = titulo.replace("        ", "") + """

DE: """ + discount_price[0] + """
PARA: """ + total_price[1] + " " + percentage_discount + "OFF" + """

""" + image_source
else:
    final_text = titulo.replace("        ", "") + """

POR APENAS: """ + total_price[1] + """

""" + image_source

print(final_text)