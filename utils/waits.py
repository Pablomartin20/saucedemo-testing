from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def is_visible(driver, locator, timeout=10):
  try:
    WebDriverWait(driver, timeout).until(
      EC.visibility_of_element_located(locator)
    )
    return True
  except TimeoutException:
    return False

def visible_and_contains_text(driver, locator, text, timeout=10):
  try:
    WebDriverWait(driver, timeout).until(
      EC.visibility_of_element_located(locator)
    )
    WebDriverWait(driver, timeout).until(
      EC.text_to_be_present_in_element(locator, text)
    )
    return True
  except TimeoutException:
    return False