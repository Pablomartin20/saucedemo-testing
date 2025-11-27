import pytest
from pages.inventory_page import InventoryPage
from utils.data_loader import load_data
from utils.texts import get_item_id

gdata = load_data("data/test_general_data.json")
pdata = load_data("data/test_products_data.json")

@pytest.mark.no_login
def test_inventario_sin_login(driver):
  inventory_page = InventoryPage(driver)
  inv_url = gdata["urls"]["inventory_url"]
  login_url = gdata["urls"]["base_url"]
  error = gdata["error_messages"]["inventory"]
  inventory_page.open(inv_url)

  assert inventory_page.is_this_error_present(error), \
    "El error no es el esperado."
  assert inventory_page.driver.current_url == login_url, \
    "La url no es la correcta."

def test_cantidad_correcta(driver):
  inventory_page = InventoryPage(driver)
  items = inventory_page.get_inventory()

  assert len(items) == pdata["expected"]["total"], \
  "La cantidad de productos no es la correcta."

def test_estan_todos_los_productos(driver):
  inventory_page = InventoryPage(driver)
  json_products = pdata["expected"]["products"]

  for i in range(0,6):
    name = inventory_page.get_product_name(i)
    found = any(
      name == prod["name"] for prod in json_products
    )

    assert found, \
    f"El producto '{name}' no coincide con los datos esperados."


def test_links_correctos(driver):
  inventory_page = InventoryPage(driver)

  for i in range(0,6):
    items = inventory_page.get_inventory()
    product_name_web = inventory_page.get_product_name(i)
    inventory_page.click_product_link(items[i])
    item_id = get_item_id(driver.current_url)
    product_name_ddbb = pdata["expected"]["products"][item_id]["name"]

    assert product_name_web == product_name_ddbb, "El link no es el correcto."

    inventory_page.previous_page()

def test_producto_inexistente(driver):
  inventory_page = InventoryPage(driver)
  inventory_page.open(gdata["urls"]["inventory_item_url"] + "8")

  assert inventory_page.item_has_this_name(gdata["error_messages"]["not_found"]), \
  "El producto no es inexistente."

def test_se_modifica_boton_agregar(driver):
  inventory_page = InventoryPage(driver)
  inventory_page.add_or_remove_product(4)
  items = inventory_page.get_inventory()

  assert inventory_page.item_can_be_removed_or_added(items[4], "Remove"), \
  "El texto del botón no es 'Remove'."

def test_quitar_desde_carrito_y_verificar(driver):
  inventory_page = InventoryPage(driver)
  inventory_page.add_or_remove_product(3)
  inventory_page.click_cart_button()
  #En el carrito get_inventory() también devuelve los items agregados
  item = inventory_page.get_inventory()[0]
  inventory_page.remove_cart_item(item)
  inventory_page.previous_page()

  #Vuelvo a obtener el item del inventario
  item = inventory_page.get_inventory()[0]

  assert inventory_page.item_can_be_removed_or_added(item, "Add to cart"), \
  "El texto del botón no es 'Add to cart'."

def test_agregar_todos_y_quitar(driver):
  inventory_page = InventoryPage(driver)
  items = inventory_page.get_inventory()

  for i in range(0,6):
    inventory_page.add_or_remove_product(i)
    assert inventory_page.item_can_be_removed_or_added(items[i], "Remove"), \
    "El texto del botón no es 'Remove'."
  
  for i in range(0,6):
    inventory_page.add_or_remove_product(i)
    assert inventory_page.item_can_be_removed_or_added(items[i], "Add to cart"), \
    "El texto del botón no es 'Add to cart'."

def test_modifica_contador_carrito(driver):
  inventory_page = InventoryPage(driver)
  
  for i in range(0,6):
    inventory_page.add_or_remove_product(i)
    assert inventory_page.get_cart_counter() == i+1, \
    "El contador del carrito no es correcto."

def test_orden_A_Z(driver):
  inventory_page = InventoryPage(driver)
  names = inventory_page.get_product_names()
  inventory_page.order("az")
  ordered_names = inventory_page.get_product_names()

  assert ordered_names == sorted(names), \
  "Los elementos no están ordenados de manera AZ correctamente."

def test_orden_Z_A(driver):
  inventory_page = InventoryPage(driver)
  names = inventory_page.get_product_names()
  inventory_page.order("za")
  ordered_names = inventory_page.get_product_names()

  assert ordered_names == sorted(names, reverse=True), \
  "Los elementos no están ordenados de manera ZA correctamente."

def test_precios_lo_hi(driver):
  inventory_page = InventoryPage(driver)
  prices = inventory_page.get_product_prices()
  inventory_page.order("lohi")
  ordered_prices = inventory_page.get_product_prices()

  assert ordered_prices == sorted(prices), \
  "Los precios no están ordenados de manera 'lohi' correctamente."

def test_precios_hi_lo(driver):
  inventory_page = InventoryPage(driver)
  prices = inventory_page.get_product_prices()
  inventory_page.order("hilo")
  ordered_prices = inventory_page.get_product_prices()

  assert ordered_prices == sorted(prices, reverse=True), \
  "Los precios no están ordenados de manera 'hilo' correctamente."