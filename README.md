## Índice

- [📖 Introducción](#introducción)
- [🗂️ Estructura del proyecto](#estructura-del-proyecto)
- [🛠️ Tecnologías y herramientas utilizadas en el desarrollo](#tecnologías-y-herramientas-utilizadas-en-el-desarrollo)
- [⚙️ Instalación y ejecución](#instalación-y-ejecución)
- [🧪 Casos de prueba implementados](#casos-de-prueba-implementados)

## Introducción

La idea de este proyecto es aplicar los conocimientos de testing manual y automatizado adquiridos en la Diplomatura en Control de Calidad de Software (UNTREF), desarrollando un conjunto de pruebas 
automatizadas sobre la plataforma SauceDemo utilizando Python, Selenium y Pytest. Incluye casos de prueba positivos y negativos que validan del correcto funcionamiento de distintos flujos de la plataforma.

## Estructura del proyecto

```
saucedemo-testing/
│
├── data/                         # JSON que simulan la base de datos de entrada y salida
│   ├── test_general_data.json
│   └── test_general_data.json
│
├── pages/                         # Page Object Model (POM)
│   ├── cart_page.py
│   ├── inventory_page.py
│   └── login_page.py
│
├── screenshots/                   # Screenshots generados por Selenium en caso fallar un test case
│
├── tests/                         # Carpeta principal de tests
│   ├── cart/
│   │   ├── conftest.py            # Configuraciones particulares para los tests del carrito
│   │   └── test_cart.py           # Test cases del carrito
│   ├── inventory/
│   │   ├── conftest.py            # Configuraciones particulares para los tests del inventario
│   │   └── test_inventory.py      # Test cases del inventario
│   ├── login/
│   │   └── test_login.py          # Test cases del login
│
├── utils/
│   ├── data_loader.py             # Función para cargar datos desde un .json
│   ├── drivers_factory.py         # Crea y configura el navegador (Chrome/Firefox)
│   ├── numbers.py                 # Funciones útiles que procesan números
│   ├── texts.py                   # Funciones útiles que procesan strings
│   └── waits.py                   # Funciones útiles que utilizan esperas explícitas
│
├── requirements.txt               # Dependencias del proyecto
├── conftest.py                    # Configuraciones y fixtures de Pytest
├── pytest.ini                     # Configuración adicional de Pytest
└── README.md                      # Documentación del proyecto
```

## Tecnologías y herramientas utilizadas en el desarrollo

- Python 3.13
- Selenium WebDriver
- Pytest con Pytest-html
- Visual Studio Code
- Git/GitHub

## Instalación y ejecución

1. Clonar el repositorio y abrirlo:
   ```bash
   git clone https://github.com/Pablomartin20/saucedemo-testing.git
   cd saucedemo-testing

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt

3. Ejecutar tests:

   Con reporte y en modo *headless* (Chrome es el navegador por default):
   ```bash
   pytest --headless --html=report.html
   ```
   
   Lo mismo pero con Firefox:
   ```bash
   pytest --headless --html=report.html --browser="firefox"
   ```
   
## Casos de prueba implementados

### 1. Login
- Login exitoso.
- Login con contraseña incorrecta.
- Login con un usuario bloqueado.
- Login con un usuario no registrado.
- Login sin escribir un usuario.
- Login sin escribir una contraseña.
- Login sin escribir ni usuario ni contraseña.

### 2. Inventario
- Acceder al inventario sin loguearse.
- Validar si el inventario tiene la cantidad correcta de ítems.
- Validar si el inventario tiene los ítems correctos.
- Validar los links de los ítems.
- Intentar acceder a un producto que no existe.
- Validar si el botón de "Agregar al carrito" cambia al presionarlo.
- Validar si el botón de "Agregar al carrito" regresa a ese estado si se elimina el producto desde el carrito.
- Agregar todos los productos al carrito y luego quitarlos para validar si los botones se comportan de la manera esperada.
- Validar si se modifica el contador del carrito al agregar algunos ítems.
- Ordenar los productos alfabéticamente (A-Z).
- Ordenar los productos alfabéticamente (Z-A).
- Ordenar los productos por precio (Low-High).
- Ordenar los productos por precio (High-Low).

### 3. Carrito de compras (el checkout es considerado parte del carrito en mi proyecto)
- Acceder al carrito sin loguearse.
- Agregar un producto y verificar si está en el carrito.
- Agregar varios productos y verificar si están en el carrito.
- Validar si el carrito persiste luego de realizar una navegación por la plataforma.
- Validar si el ítem desaparece del carrito luego de eliminarlo desde el detalle del producto.
- Validar si el carrito persiste luego de cerrar sesión y volver a iniciarla.
- Validar si los precios unitarios de los ítems agregados son los mismos en el carrito.
- Validar si el subtotal, los impuestos y el total del carrito son los correctos.
