from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.texts import float_price
from utils.waits import visible_and_contains_text

class InventoryPage:
  def __init__(self, driver):
    self.driver = driver

  #Acciones
  def open(self, url):
    self.driver.get(url)

  def previous_page(self):
    return self.driver.back()

  def add_or_remove_product(self, item):
    product_buttons = self.driver.find_elements(By.XPATH, "//div[@class='pricebar']//button")
    product_buttons[item].click()
  
  def get_inventory(self):
    return self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item']")
  
  def click_cart_button(self):
    container = self.driver.find_element(By.ID, "shopping_cart_container")
    container.find_element(By.TAG_NAME, "a").click()
    
  def click_product_link(self, product):
    product.find_element(By.TAG_NAME, "a").click()
  
  def get_product_name(self, item):
    items = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item-name']")
    return items[item].text
  
  def get_product_names(self):
    names = []
    for i in range(0,6):
      name = self.get_product_name(i)
      names.append(name)
    return names
  
  def get_product_price(self, item):
    items = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item-price']")
    return items[item].text.strip()
  
  def get_product_prices(self):
    prices = []
    for i in range(0,6):
      price = self.get_product_price(i)
      prices.append(float_price(price))
    return prices
  
  def remove_cart_item(self, item):
    button = item.find_element(By.TAG_NAME, "button")
    button.click()
  
  def get_cart_counter(self):
    counter = self.driver.find_element(By.XPATH, "//span[@data-test='shopping-cart-badge']")
    return int(counter.text)
  
  def order(self, order_type):
    find = self.driver.find_element(By.XPATH, "//select[@data-test='product-sort-container']")
    select = Select(find)
    select.select_by_value(order_type)

  #Verificaciones
  def is_this_error_present(self, text):
    #Vemos si el mensaje de error aparece para verificar
    locator = (By.XPATH, "//h3[@data-test='error']")
    return visible_and_contains_text(self.driver, locator, text)
  
  def item_has_this_name(self, name):
    item_name = self.driver.find_element(By.XPATH, "//div[@data-test='inventory-item-name']")
    return item_name.text == name
  
  def item_can_be_removed_or_added(self, item, text):
    text_button = item.find_element(By.TAG_NAME, "button").text
    return text_button == text