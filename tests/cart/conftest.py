import pytest
from pages.login_page import LoginPage
from utils.data_loader import load_data

data = load_data("data/test_general_data.json")

@pytest.fixture(autouse=True)
def login(driver, request):
  if "no_login" in request.keywords:
    yield #Nos saltamos el login si está el marcador
    return
  
  login_page = LoginPage(driver)
  login_page.open(data["urls"]["inventory_url"])
  valid_user = data["valid_users"][0]
  login_page.login(valid_user["username"], valid_user["password"])
  yield login