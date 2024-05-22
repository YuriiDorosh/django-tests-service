import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
            
            return add_to_cart_url
            
            # if add_to_cart_url:
            #     checkout_url = complete_checkout(add_to_cart_url)
            #     if checkout_url:
            #         driver.quit()
            #         return checkout_url
            #     else:
            #         driver.quit()
            #         return False
            # else:
            #     driver.quit()
            #     return False
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
        
        try:
            # Fill the text fields
            driver.find_element(By.ID, "fname").send_keys("Іван")
            driver.save_screenshot("./complete_checkout_fname.png")
            driver.find_element(By.ID, "lname").send_keys("Петров")
            driver.save_screenshot("./complete_checkout_lname.png")
            driver.find_element(By.ID, "patronymic").send_keys("Михайлович")
            driver.save_screenshot("./complete_checkout_patronymic.png")
            driver.find_element(By.ID, "Phone").send_keys("+380123456789")
            driver.save_screenshot("./complete_checkout_Phone.png")
            driver.find_element(By.ID, "email").send_keys("ivan.petrov@example.com")
            driver.save_screenshot("./complete_checkout_email.png")
            driver.find_element(By.ID, "comment").send_keys("Будь ласка, доставте після 16:00.")
            driver.save_screenshot("./complete_checkout_comment.png")

            # Choose city
            city_input = driver.find_element(By.ID, "city")
            city_input.click()
            time.sleep(2)  # Ensure dropdown interaction time
            city_input.send_keys("Львів")
            time.sleep(5)  # Wait for the dropdown to populate
            city_input.send_keys(Keys.DOWN)  # Navigate to the first entry
            city_input.send_keys(Keys.RETURN)
            driver.save_screenshot("./complete_checkout_choose_lviv.png")

            # Choose post office
            post_office_input = driver.find_element(By.ID, "post_office")
            post_office_input.click()
            time.sleep(2)  # Ensure dropdown interaction time
            post_office_input.send_keys(Keys.DOWN)  # Navigate to the first entry
            time.sleep(5)  # Ensure dropdown interaction time
            post_office_input.send_keys(Keys.RETURN)
            driver.save_screenshot("./complete_checkout_post_office.png")

            # Click the order submission button
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "s_btn"))
            )
            submit_button.click()
            time.sleep(3)  # Wait for any processing
            
            driver.save_screenshot("./complete_checkout_final.png")  # Final screenshot after submitting
            
            current_url = driver.current_url

            return current_url

            return True
        except Exception as e:
            print(f"Error during checkout: {str(e)}")
            return False

        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        return False

    finally:
        driver.quit()


# def complete_checkout(url):
    
#     webdriver_setup = WebDriverSetup()
#     driver = webdriver_setup.get_driver()

#     driver.get(url)
#     driver.save_screenshot("./complete_checkout_start.png")
#     try:
#         # Fill the text fields
#         driver.find_element(By.ID, "fname").send_keys("Іван")
#         driver.save_screenshot("./complete_checkout_fname.png")
#         driver.find_element(By.ID, "lname").send_keys("Петров")
#         driver.save_screenshot("./complete_checkout_lname.png")
#         driver.find_element(By.ID, "patronymic").send_keys("Михайлович")
#         driver.save_screenshot("./complete_checkout_patronymic.png")
#         driver.find_element(By.ID, "Phone").send_keys("+380123456789")
#         driver.save_screenshot("./complete_checkout_Phone.png")
#         driver.find_element(By.ID, "email").send_keys("ivan.petrov@example.com")
#         driver.save_screenshot("./complete_checkout_email.png")
#         driver.find_element(By.ID, "comment").send_keys("Будь ласка, доставте після 16:00.")
#         driver.save_screenshot("./complete_checkout_comment.png")

#         # Choose city
#         city_input = driver.find_element(By.ID, "city")
#         city_input.click()
#         city_input.send_keys("Львів")
#         time.sleep(2)  # Wait for the dropdown to populate
#         city_input.send_keys(Keys.DOWN)  # Navigate to the first entry
#         city_input.send_keys(Keys.RETURN)
#         driver.save_screenshot("./complete_checkout_choose_lviv.png")

#         # Choose post office
#         post_office_input = driver.find_element(By.ID, "post_office")
#         post_office_input.click()
#         post_office_input.send_keys(Keys.DOWN)  # Navigate to the first entry
#         time.sleep(1)  # Ensure dropdown interaction time
#         post_office_input.send_keys(Keys.RETURN)
#         driver.save_screenshot("./complete_checkout_post_office.png")

#         # Click the order submission button
#         submit_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, "s_btn"))
#         )
#         submit_button.click()
#         time.sleep(3)  # Wait for any processing
        
#         driver.save_screenshot("./complete_checkout_final.png")  # Final screenshot after submitting

#         return True

#     except Exception as e:
#         print(f"Error during checkout: {str(e)}")
#         return False
