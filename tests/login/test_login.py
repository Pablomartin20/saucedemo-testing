import pytest
from pages.login_page import LoginPage
from utils.data_loader import load_data

data = load_data("data/test_general_data.json")

def do_login(driver, base_url, username, password):
  login_page = LoginPage(driver)
  login_page.open(base_url)
  login_page.login(username, password)

  return login_page

@pytest.mark.parametrize("cred", data["valid_users"])
def test_login_correcto(driver, cred):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, cred["username"], cred["password"])

  assert login_page.is_logged(), \
  f"El login para el usuario {cred["username"]} falló."

@pytest.mark.parametrize("cred", data["valid_users"])
def test_login_contrasena_incorrecta(driver, cred):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, cred["username"], "asdasdasd1234")
  text = data["error_messages"]["invalid_user"]

  assert login_page.is_this_error_present(text), \
  f"La contraseña incorrecta para el usuario {cred["username"]} no mostró el mensaje esperado."

@pytest.mark.parametrize("cred", data["locked_users"])
def test_login_usuario_bloqueado(driver, cred):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, cred["username"], cred["password"])
  text = data["error_messages"]["locked_user"]

  assert login_page.is_this_error_present(text), \
  f"El usuario bloqueado {data["username"]} no mostró el mensaje esperado."

@pytest.mark.parametrize("cred", data["unregistered_users"])
def test_login_usuario_no_registrado(driver, cred):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, cred["username"], cred["password"])
  text = data["error_messages"]["invalid_user"]

  assert login_page.is_this_error_present(text), \
  f"El usuario no registrado {data["username"]} no mostró el mensaje esperado."

def test_login_sin_usuario(driver):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, "", "secret_sauce")
  text = data["error_messages"]["no_user"]

  assert login_page.is_this_error_present(text), \
  f"El intento de loguearse sin usuario no mostró el mensaje esperado."

@pytest.mark.parametrize("cred", data["valid_users"])
def test_login_sin_contrasena(driver, cred):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, cred["username"], "")
  text = data["error_messages"]["no_password"]

  assert login_page.is_this_error_present(text), \
  f"El intento de loguearse sin contraseña no mostró el mensaje esperado."

def test_login_sin_usuario_ni_contrasena(driver):
  url = data["urls"]["base_url"]
  login_page = do_login(driver, url, "", "")
  text = data["error_messages"]["no_user"]

  #Se agregó un espacio al propósito para crear un screenshot
  assert login_page.is_this_error_present(text + " "), \
  f"El intento de loguearse sin usuario ni contraseña no mostró el mensaje esperado."