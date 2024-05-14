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
            
            new_url = open_first_item(current_url)
            
            driver.quit()
            return new_url
        except Exception as e:
            driver.quit()
            return False


def open_first_item(url):
    # Initialize WebDriver using the setup class
    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()

    # Load the webpage
    driver.get(url)

    try:
        # Wait for the page to load and click the first item in the category
        first_item = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".categories-item a"))
        )
        first_item.click()

        # Optionally, print or return the current URL
        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()