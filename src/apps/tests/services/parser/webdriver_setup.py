from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSetup:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.service = Service(ChromeDriverManager().install())

    def get_driver(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.set_window_size(1920, 1080)
        return driver
