from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Todo 3: Get the most expensive upgrade once Available
def buy_upgrade(money):
    # Get all the upgrades prices
    store_tag = driver.find_elements(By.CSS_SELECTOR, value="#store b")
    # store has an extra element with no data, that is why it has to be in range and not in items
    store_prices = [int(store_tag[n].text.split("-")[1].strip(" ").replace(',', '')) for n in range(8)]
    store_prices_reversed = list(reversed(store_prices))
    store_items = [store_tag[n].text.split("-")[0].strip(" ") for n in range(8)]
    store_items_reversed = list(reversed(store_items))
    for items in store_prices_reversed:
        if money > items:
            option = store_prices_reversed.index(items)
            driver.find_element(By.ID, value=f"buy{store_items_reversed[option]}").click()
            money = 0


# Todo 1: Connect Selenium to browser website and keep it open

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url='https://orteil.dashnet.org/experiments/cookie/')

# todo 2: Pinpoint the cookie and Click on it repeatedly

cookie = driver.find_element(By.ID, value="cookie")
# EXECUTE THE LOOP AT THE SPECIFIC AMOUNT OF TIME (TIMEOUT)
timeout = time.time() + 60 * 5
# ADDS 5 SECONDS
update_time = time.time() + 5
while time.time() < timeout:
    cookie.click()
    cookie_money = int(driver.find_element(By.ID, value='money').text)
    # Todo 4: Get the upgrade every 5 seconds
    if time.time() > update_time:
        buy_upgrade(cookie_money)
        update_time = time.time() + 5
# Todo 5: After 5 minutes have passed since starting the game, stop the bot and print the "cookies/second"
cookies_second = driver.find_element(By.ID, value='cps')
print(cookies_second.text)
driver.close()
