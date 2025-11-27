from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def create_driver(browser, headless=False):
  if browser == "chrome":
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
      "profile.password_manager_leak_detection": False
    })
    if headless:
      options.add_argument("--headless=new")
    return webdriver.Chrome(service=ChromeService(), options=options)
  
  elif browser == "firefox":
    options = FirefoxOptions()
    options.add_argument("--start-maximized")
    if headless:
      options.add_argument("--headless")
    return webdriver.Firefox(service=FirefoxService(), options=options)
  
  else:
    raise ValueError("Navegador no soportado.")