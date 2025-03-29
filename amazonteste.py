from AmazonScraping import ScrapingAmazon

scraping = ScrapingAmazon(link="https://amzn.to/4k6dVlz")

soup = scraping.requestSelenium()
core_price = scraping.corePrice(soup)

total_price = scraping.totalPrice(core_price)
discount_verify = scraping.discountVerify(core_price)

discount_price = []
percentage_discount = ""

image_source = scraping.image_source(soup)

if discount_verify:
    discount_price = scraping.discountPrice(core_price)
    percentage_discount = scraping.percentageDiscount(core_price)

titulo = scraping.title(soup)

print(titulo)