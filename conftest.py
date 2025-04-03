import pytest
import platform
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# WebDriver Manager config for Mac ARM 64
os.environ["WDM_ARCHITECTURE"] = "arm64" if platform.processor() == "arm" else "x64"

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
    