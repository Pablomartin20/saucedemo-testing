import json

def load_data(ruta):
  with open(ruta) as f:
    return json.load(f)