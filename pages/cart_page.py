from selenium.webdriver.common.by import By
from utils.waits import is_visible, visible_and_contains_text
from utils.texts import float_price, float_item_subtotal, float_tax, float_cart_total
from utils.numbers import round_up

class CartPage:
  def __init__(self, driver):
    self.driver = driver
  
  #Acciones
  def open(self, url):
    self.driver.get(url)
  
  def previous_page(self):
    return self.driver.back()
  
  def add_or_remove_from_inventory(self, item):
    product_buttons = self.driver.find_elements(By.XPATH, "//div[@class='pricebar']//button")
    product_buttons[item].click()
  
  def click_cart_button(self):
    container = self.driver.find_element(By.ID, "shopping_cart_container")
    container.find_element(By.TAG_NAME, "a").click()
  
  def get_product_name(self, item):
    items = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item-name']")
    return items[item].text

  def click_cart_item(self, item):
    items = self.driver.find_elements(By.XPATH, "//div[@class='cart_item_label']/a")
    items[item].click()
  
  def click_continue_shopping(self):
    self.driver.find_element(By.ID, "continue-shopping").click()

  def remove_from_detail(self):
    self.driver.find_element(By.ID, "remove").click()
  
  def get_inventory_quantity(self):
    inv = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item']")
    return len(inv)
  
  def click_inventory_item(self, item):
    products = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item-description']//a")
    products[item].click()
  
  def get_product_price(self, item):
    items = self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item-price']")
    return float_price(items[item].text.strip())

  def logout(self):
    self.driver.find_element(By.ID, "react-burger-menu-btn").click()
    if is_visible(self.driver, (By.ID, "logout_sidebar_link")):
      self.driver.find_element(By.ID, "logout_sidebar_link").click()
  
  def get_item_subtotal(self):
    subtotal = self.driver.find_element(By.XPATH, "//div[@data-test='subtotal-label']")
    return float_item_subtotal(subtotal.text)
  
  def get_tax(self):
    tax = self.driver.find_element(By.XPATH, "//div[@data-test='tax-label']")
    return float_tax(tax.text)
  
  def get_total(self):
    total = self.driver.find_element(By.XPATH, "//div[@data-test='total-label']")
    return float_cart_total(total.text)

  def checkout(self):
    self.driver.find_element(By.ID, "checkout").click()
    self.driver.find_element(By.ID, "first-name").send_keys("Fulanito")
    self.driver.find_element(By.ID, "last-name").send_keys("Perez")
    self.driver.find_element(By.ID, "postal-code").send_keys("1234")
    self.driver.find_element(By.ID, "continue").click()
  
  def calculate_tax(self, subtotal):
    return round_up(subtotal * 0.08)

  #Verificaciones
  def is_this_error_present(self, text):
    locator = (By.XPATH, "//h3[@data-test='error']")
    return visible_and_contains_text(self.driver, locator, text)