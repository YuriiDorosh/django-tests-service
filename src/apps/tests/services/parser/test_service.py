import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .webdriver_setup import WebDriverSetup

def parse_and_click_button(url, button_text):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        webdriver_setup = WebDriverSetup()
        driver = webdriver_setup.get_driver() 

        # Load the webpage
        driver.get(url)
        
        try:
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Матраци"))
            )
            link.click()
            current_url = driver.current_url
            driver.quit()
            return current_url
        except Exception as e:
            driver.quit()
            return False
