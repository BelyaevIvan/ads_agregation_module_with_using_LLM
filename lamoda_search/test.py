from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

query = "кроссовки"
url = f"https://www.lamoda.ru/catalogsearch/result/?q={query}"
driver.get(url)

cards = driver.find_elements(By.CSS_SELECTOR, "div.x-product-card__link")
for card in cards:
    name = card.find_element(By.CSS_SELECTOR, ".x-product-card-description__product-name").text
    price = card.find_element(By.CSS_SELECTOR, "._price_163e7_8.x-product-card-description__price-new").text
    img = card.find_element(By.CSS_SELECTOR, "img.x-product-card__pic-img").get_attribute("src")
    print({"name": name, "price": price, "image": img})

driver.quit()
