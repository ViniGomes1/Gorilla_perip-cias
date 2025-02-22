from MercadoLivreScraping import ScrapingML

link = "https://mercadolivre.com/sec/2WXZqrh"

#https://mercadolivre.com/sec/1pwcgie

link2 = "https://mercadolivre.com/sec/1SQ9LGG"

scraping = ScrapingML(link2)
requesting = scraping.request()

money_fractions = scraping.find_children(requesting, 'andes-money-amount__fraction', True)
discount = scraping.find_children(requesting, 'poly-price__installments', False)

image_link = scraping.link
product_title = scraping.title(requesting)
amount_discount = scraping.amount_discount(requesting)


product_final = image_link + """ 

""" + product_title + """

DE: """ + money_fractions[0] + """
POR: """ + money_fractions[1] + " " + amount_discount + """
""" + discount[0].text

print(product_final)


