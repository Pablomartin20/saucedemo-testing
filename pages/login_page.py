from selenium.webdriver.common.by import By
from utils.waits import is_visible, visible_and_contains_text

class LoginPage:
  def __init__(self, driver):
    self.driver = driver

  #Acciones
  def open(self, url):
    self.driver.get(url)

  def login(self, username, password):
    self.driver.find_element(By.ID, "user-name").send_keys(username)
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "login-button").click()
  
  #Verificaciones
  def is_logged(self):
    #Vemos si está el menú hamburguesa para verificar
    locator = (By.ID, "react-burger-menu-btn")
    return is_visible(self.driver, locator)

  def is_this_error_present(self, text):
    #Vemos si el mensaje de error aparece para verificar
    locator = (By.XPATH, "//h3[@data-test='error']")
    return visible_and_contains_text(self.driver, locator, text)