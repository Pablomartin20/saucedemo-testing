import pytest
import os
from datetime import datetime
from utils.drivers_factory import create_driver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Navegador a usar: chrome o firefox")
    parser.addoption("--headless", action="store_true", help="Ejecutar en modo headless")

@pytest.fixture
def driver(request):
  #Setup
  browser = request.config.getoption("--browser")
  headless = request.config.getoption("--headless")
  driver = create_driver(browser, headless)
  #yield driver
  #Teardown
  def teardown():
    try:
      driver.quit()
    except Exception as e:
      print(f"Error al cerrar el driver: {e}")
  request.addfinalizer(teardown)
  return driver

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()

  if report.failed and "driver" in item.fixturenames:
    driver = item.funcargs["driver"]

    # Crear carpeta si no existe
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
      os.makedirs(screenshots_dir)

    # Nombre del archivo
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    nodeid_clean = report.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
    file_name = f"{nodeid_clean}_{timestamp}.png"
    file_path = os.path.join(screenshots_dir, file_name)

    # Guardar screenshot
    try:
      driver.save_screenshot(file_path)
      print(f"Screenshot guardado: {file_path}")
    except Exception as e:
      print(f"No se pudo guardar el screenshot: {e}")