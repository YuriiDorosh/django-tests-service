import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .webdriver_setup import WebDriverSetup
from .test_errors_handle import handle_errors
import time


def parse_and_click_button(url, button="Матраци"):
    errors = []
    response = requests.get(url)

    if response.status_code != 200:
        return None, ["Failed to load URL"]

    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()
    driver.get(url)

    try:
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, button))
        )
        link.click()
        current_url = driver.current_url

        first_item_url, error = open_first_item(current_url)
        if error:
            errors.append(error)
            return None, errors

        add_to_cart_url, error = add_to_cart(first_item_url)
        
        if error:
            errors.append(error)
            return None, errors
            
        return add_to_cart_url, None
            
    except Exception as e:
        driver.quit()
        return False
 
    finally:
        driver.quit()

@handle_errors
def open_first_item(url):
    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()

    driver.get(url)

    try:
        first_item = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".categories-item a"))
        )
        first_item.click()

        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

@handle_errors
def add_to_cart(url):
    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()

    driver.get(url)

    try:
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
        )
        buy_button.click()

        time.sleep(3)

        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.popup-buy__footer-btn")
        )
        driver.save_screenshot("./before1.png")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout_link"))
        )
        checkout_link = driver.find_element(By.ID, "checkout_link")
        checkout_url = checkout_link.get_attribute("href")

        driver.get(checkout_url)
        time.sleep(3)
        
        try:
            driver.find_element(By.ID, "fname").send_keys("test")
            driver.find_element(By.ID, "lname").send_keys("test")
            driver.find_element(By.ID, "patronymic").send_keys("test")
            driver.find_element(By.ID, "Phone").send_keys("+380123456789")
            driver.find_element(By.ID, "email").send_keys("test.test@example.com")
            driver.find_element(By.ID, "comment").send_keys("###12")

            city_input = driver.find_element(By.ID, "city")
            city_input.click()
            time.sleep(2)  
            city_input.send_keys("Львів")
            time.sleep(5)  
            city_input.send_keys(Keys.DOWN)  
            city_input.send_keys(Keys.RETURN)

            """ цього поки нема бо баг з вибором міста(можна нажати ентер і воно вже відправить)

            # # Choose post office
            # post_office_input = driver.find_element(By.ID, "post_office")
            # post_office_input.click()
            # time.sleep(2)  # Ensure dropdown interaction time
            # post_office_input.send_keys(Keys.DOWN)  # Navigate to the first entry
            # time.sleep(5)  # Ensure dropdown interaction time
            # post_office_input.send_keys(Keys.RETURN)
            # driver.save_screenshot("./complete_checkout_post_office.png")

            # # Click the order submission button
            # submit_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, "s_btn"))
            # )
            # submit_button.click()
            # time.sleep(3)  # Wait for any processing
            
            """
                  
            current_url = driver.current_url

            return current_url

        except Exception as e:
            print(f"Error during checkout: {str(e)}")
            return False

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        return False

    finally:
        driver.quit()