import pytest
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from utils.data_loader import load_data

gdata = load_data("data/test_general_data.json")
pdata = load_data("data/test_products_data.json")

@pytest.mark.no_login
def test_carrito_sin_login(driver):
  cart_page = CartPage(driver)
  cart_url = gdata["urls"]["cart_url"]
  login_url = gdata["urls"]["base_url"]
  error = gdata["error_messages"]["cart"]
  cart_page.open(cart_url)

  assert cart_page.is_this_error_present(error), \
    "El error no es el esperado."
  assert cart_page.driver.current_url == login_url, \
    "La url no es la correcta."

def test_agrega_uno(driver):
  cart_page = CartPage(driver)
  name_in_inv = cart_page.get_product_name(2)
  cart_page.add_or_remove_from_inventory(2)
  cart_page.click_cart_button()
  name_in_cart = cart_page.get_product_name(0)

  assert name_in_inv == name_in_cart, \
  "El producto agregado al carrito no es el mismo."

def test_agrega_varios(driver):
  cart_page = CartPage(driver)
  names_in_inv = []

  for i in range(0,3):
    cart_page.add_or_remove_from_inventory(i)
    names_in_inv.append(cart_page.get_product_name(i))
  
  cart_page.click_cart_button()

  for i in range(0,3):
    name_in_cart = cart_page.get_product_name(i)
    assert name_in_cart == names_in_inv[i], \
    f"El producto '{name_in_cart}' agregado al carrito no es el mismo que en inventario."

def test_persistencia_carrito_navegacion(driver):
  cart_page = CartPage(driver)
  cart_page.add_or_remove_from_inventory(0)
  name_in_inv = cart_page.get_product_name(0)
  cart_page.click_cart_button()
  cart_page.click_continue_shopping()
  cart_page.click_inventory_item(5)
  cart_page.previous_page()
  cart_page.click_cart_button()
  name_in_cart = cart_page.get_product_name(0)

  assert name_in_inv == name_in_cart, \
  "No hubo persistencia del carrito en la navegación."

def test_elimina_desde_detalle(driver):
  cart_page = CartPage(driver)
  cart_page.add_or_remove_from_inventory(0)
  cart_page.click_cart_button()
  cart_page.click_cart_item(0)
  cart_page.remove_from_detail()
  cart_page.click_cart_button()

  assert cart_page.get_inventory_quantity() == 0, \
  "El elemento no se eliminó."

def test_persistencia_carrito_logout(driver):
  cart_page = CartPage(driver)
  cart_page.add_or_remove_from_inventory(1)
  name_in_inv = cart_page.get_product_name(1)
  cart_page.logout()
  login_page = LoginPage(driver)
  login_page.login("standard_user", "secret_sauce")
  cart_page.click_cart_button()
  name_in_cart = cart_page.get_product_name(0)

  assert name_in_inv == name_in_cart, \
  "El producto no se mantuvo luego del log out."

#El checkout lo considero parte del carrito
def test_precios_unitarios_correctos(driver):
  cart_page = CartPage(driver)
  cart_page.add_or_remove_from_inventory(1)
  price_1_in_inv = cart_page.get_product_price(1)
  cart_page.add_or_remove_from_inventory(5)
  price_2_in_inv = cart_page.get_product_price(5)
  cart_page.add_or_remove_from_inventory(3)
  price_3_in_inv = cart_page.get_product_price(3)
  cart_page.click_cart_button()
  #Considero el checkout de saucedemo como parte del carrito
  cart_page.checkout()
  price_1_in_cart = cart_page.get_product_price(0)
  price_2_in_cart = cart_page.get_product_price(1)
  price_3_in_cart = cart_page.get_product_price(2)

  assert price_1_in_inv == price_1_in_cart and price_2_in_inv == price_2_in_cart and \
  price_3_in_inv == price_3_in_cart, "Algún precio unitario no coincide."

def test_subtotal_impuesto_y_total_correctos(driver):
  cart_page = CartPage(driver)
  cart_page.add_or_remove_from_inventory(0)
  price_1_in_inv = cart_page.get_product_price(0)
  cart_page.add_or_remove_from_inventory(2)
  price_2_in_inv = cart_page.get_product_price(2)
  cart_page.add_or_remove_from_inventory(3)
  price_3_in_inv = cart_page.get_product_price(3)
  cart_page.click_cart_button()
  cart_page.checkout()

  subtotal_calc = price_1_in_inv + price_2_in_inv + price_3_in_inv
  tax_calc = cart_page.calculate_tax(subtotal_calc)
  total_calc = tax_calc + subtotal_calc

  assert cart_page.get_item_subtotal() == subtotal_calc, \
  "Los subtotales no coinciden."
  assert cart_page.get_tax() == tax_calc, \
  "Los impuestos no coinciden."
  assert cart_page.get_total() == total_calc, \
  "Los totales no coinciden."