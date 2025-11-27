from urllib.parse import urlparse, parse_qs

def get_item_id(url):
  parsed_url = urlparse(url)
  params = parse_qs(parsed_url.query)
  
  return int(params.get("id", [None])[0])

def float_price(str_price):
  return float(str_price.replace("$", ""))

def float_item_subtotal(str_total):
  return float(str_total.replace("Item total: $", ""))

def float_tax(str_tax):
  return float(str_tax.replace("Tax: $", ""))

def float_cart_total(str_cart):
  return float(str_cart.replace("Total: $", ""))