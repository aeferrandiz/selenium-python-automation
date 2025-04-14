import pytest
import json
import os
import platform
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def load_config():
    """Carga la configuración desde el archivo config.json"""
    # Ruta al archivo de configuración
    config_path = Path(__file__).parent.parent / 'config' / 'config.json'
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado: {config_path}")
        return {
            "browser": "chrome",
            "headless": False,
            "window_size": {"width": 1920, "height": 1080},
            "reports_path": "./reports"
        }  # Valores predeterminados

def get_timestamp():
    """Retorna un timestamp para nombrar los reportes"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

@pytest.fixture(scope="session")
def config():
    """Fixture para acceder a la configuración en las pruebas"""
    return load_config()

@pytest.fixture()
def driver(request, config):
    """Fixture principal que configura y retorna el driver de Selenium"""
    # Determinar el navegador a utilizar (prioridad: CLI, luego config.json)
    browser_from_cli = request.config.getoption("--browser")
    browser = browser_from_cli if browser_from_cli != "default" else config.get("browser", "chrome")
    
    # Obtener configuración de headless mode
    headless = request.config.getoption("--headless")
    if headless is None:  # Si no se especifica en CLI, usar la configuración del JSON
        headless = config.get("headless", False)
    
    # Obtener configuración del tamaño de ventana
    window_size = config.get("window_size", {"width": 1920, "height": 1080})
    
    print(f"Creating {browser} driver (Headless: {headless}, Size: {window_size['width']}x{window_size['height']})")
    
    # Configurar el driver según el navegador
    if browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    
    elif browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        # Detectar si estamos en macOS con ARM64 (M1/M2)
        is_arm64_mac = platform.system() == "Darwin" and platform.machine() == "arm64"
        
        if is_arm64_mac:
            # Configuración especial para Chrome en Mac con chips ARM
            driver = webdriver.Chrome(options=options)
        else:
            # Configuración estándar para otras plataformas
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
    
    else:
        raise TypeError(f"Automation does not support browser {browser}")
    
    # Configurar el tamaño de la ventana
    driver.set_window_size(window_size["width"], window_size["height"])
    
    # Configurar tiempos de espera
    driver.set_script_timeout(10)
    # Puedes descomentar esta línea si necesitas implicitly_wait
    # driver.implicitly_wait(10)
    
    yield driver
    
    print(f"Closing {browser} driver")
    driver.quit()

@pytest.fixture()
def desktop_view(driver, config):
    """Fixture para establecer una vista de escritorio"""
    desktop_size = {"width": 1920, "height": 1080}
    driver.set_window_size(desktop_size["width"], desktop_size["height"])
    return driver

@pytest.fixture()
def tablet_view(driver, config):
    """Fixture para establecer una vista de tablet"""
    tablet_size = {"width": 768, "height": 1024}
    driver.set_window_size(tablet_size["width"], tablet_size["height"])
    return driver

@pytest.fixture()
def mobile_view(driver, config):
    """Fixture para establecer una vista de móvil"""
    mobile_size = {"width": 375, "height": 812}
    driver.set_window_size(mobile_size["width"], mobile_size["height"])
    return driver

def pytest_addoption(parser):
    """Agrega opciones de línea de comandos a pytest"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="default", 
        help="Browser para testing (edge, chrome, firefox, default=valor de config.json)"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=None,
        help="Ejecutar en modo headless"
    )

def pytest_configure(config):
    """Configura el reporte HTML y otros ajustes globales"""
    # Crear carpeta de reportes si no existe
    cfg = load_config()
    
    # Convertir la ruta relativa a absoluta basada en el directorio del proyecto
    reports_path_str = cfg.get("reports_path", "./reports")
    if reports_path_str.startswith("./"):
        # Si es una ruta relativa, la hacemos relativa al directorio raíz del proyecto
        reports_path = Path(__file__).parent.parent / reports_path_str[2:]
    else:
        reports_path = Path(reports_path_str)
    
    # Crear el directorio si no existe
    reports_path.mkdir(parents=True, exist_ok=True)
    
    # Configurar la ruta del reporte HTML
    report_file = reports_path / f"report_{get_timestamp()}.html"
    config.option.htmlpath = str(report_file)
    
    # Puedes agregar más configuraciones globales aquí

'''import pytest
import platform
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Versión mejorada para detectar correctamente arquitectura en Mac con Apple Silicon
if platform.system() == "Darwin" and (platform.processor() == "arm" or "arm" in platform.machine().lower()):
    os.environ["WDM_ARCHITECTURE"] = "arm64"
else:
    os.environ["WDM_ARCHITECTURE"] = "x64"

@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser")
    print(f"Creating driver for {browser}")
    
    if browser == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    elif browser == "chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    else:
        raise TypeError(f"Automation does not support browser {browser}")
    
    driver.implicitly_wait(10)
    
    yield driver
    
    print(f"Closing driver for {browser}")
    driver.quit()

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="firefox", help="browser for testing (edge,chrome,firefox)"
    )
    '''