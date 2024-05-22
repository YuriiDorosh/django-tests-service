import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .webdriver_setup import WebDriverSetup
import time


def parse_and_click_button(url, button_text):
    response = requests.get(url)

    if response.status_code == 200:
        webdriver_setup = WebDriverSetup()
        driver = webdriver_setup.get_driver()

        driver.get(url)

        try:
            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Матраци"))
            )
            link.click()
            current_url = driver.current_url

            first_item_url = open_first_item(current_url)

            add_to_cart_url = add_to_cart(first_item_url)

            driver.quit()
            return add_to_cart_url
        except Exception as e:
            driver.quit()
            return False


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


def add_to_cart(url):
    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()

    driver.get(url)

    try:
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
        )
        buy_button.click()

        driver.save_screenshot("./buy_button_clicked.png")

        time.sleep(5)

        driver.save_screenshot("./modal_appeared.png")

        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.popup-buy__footer-btn")
        )
        driver.save_screenshot("./before1.png")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout_link"))
        )
        driver.save_screenshot("./before2.png")
        checkout_link = driver.find_element(By.ID, "checkout_link")
        checkout_url = checkout_link.get_attribute("href")
        driver.save_screenshot("./after.png")

        driver.get(checkout_url)
        time.sleep(5)
        driver.save_screenshot("./checkout_page.png")

        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        return False

    finally:
        driver.quit()
