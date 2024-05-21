import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .webdriver_setup import WebDriverSetup
from selenium.webdriver.common.action_chains import ActionChains
import time

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
            
            first_item_url = open_first_item(current_url)
            
            add_to_cart_url = add_to_cart(first_item_url)
            
            driver.quit()
            return add_to_cart_url
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
        
# def add_to_cart(url):
#     webdriver_setup = WebDriverSetup()
#     driver = webdriver_setup.get_driver()

#     # Load the product page
#     driver.get(url)

#     try:
#         # Wait until the 'Buy' button is clickable
#         buy_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
#         )
#         # Click the 'Buy' button
#         buy_button.click()
        
#         driver.save_screenshot('./buy_button_clicked.png')

#         # Optionally, handle the next steps (like navigating to the cart page or confirmation)
#         # Here, let's just return the current URL to confirm the navigation
#         current_url = driver.current_url
#         return current_url

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return False

#     finally:
#         driver.quit()

# def add_to_cart(url):
#     webdriver_setup = WebDriverSetup()
#     driver = webdriver_setup.get_driver()

#     # Load the product page
#     driver.get(url)

#     try:
#         # Wait until the 'Buy' button is clickable
#         buy_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
#         )
#         # Click the 'Buy' button
#         buy_button.click()
        
#         driver.save_screenshot('./buy_button_clicked.png')

#         # Optionally, handle the next steps (like navigating to the cart page or confirmation)
#         # Here, let's just return the current URL to confirm the navigation
#         # current_url = driver.current_url
        
#         WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popup_inner"))
#         )
        
#         current_url = driver.current_url
#         return current_url

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return False

#     finally:
#         driver.quit()

def add_to_cart(url):
    webdriver_setup = WebDriverSetup()
    driver = webdriver_setup.get_driver()

    # Load the product page
    driver.get(url)

    try:
        # Wait until the 'Buy' button is clickable
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
        )
        buy_button.click()

        # Screenshot right after clicking the Buy button
        driver.save_screenshot('./buy_button_clicked.png')

        time.sleep(5)
        
        driver.save_screenshot('./modal_appeared.png')
        
        # WebDriverWait(driver, 10).until(
        #     EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
        # )
        
        html_content = driver.page_source
        # return html_content
        
        # order_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
        # )
        # order_button.click()
        
        # time.sleep(5)
        
        # driver.save_screenshot('./order_button.png')
        
        # # html_content = driver.page_source
        # # return html_content
        
        # current_url = driver.current_url
        # return current_url
        
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
            driver.switch_to.frame(iframe)
            # Attempt to find and click the order button within the iframe
            try:
                order_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
                )
                order_button.click()
                break  # If found and clicked, break out of the loop
            except KeyError as e:
                driver.switch_to.default_content()

        time.sleep(5)
        driver.save_screenshot('./order_button.png')
        current_url = driver.current_url
        return current_url

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        return False

    finally:
        driver.quit()


# def add_to_cart(url):
#     webdriver_setup = WebDriverSetup()
#     driver = webdriver_setup.get_driver()

#     # Load the product page
#     driver.get(url)

#     try:
#         # Wait until the 'Buy' button is clickable
#         buy_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-info__btn-buy"))
#         )
#         buy_button.click()

#         # Screenshot right after clicking the Buy button
#         driver.save_screenshot('./buy_button_clicked.png')

#         time.sleep(5)
        
#         driver.save_screenshot('./modal_appeared.png')
        
#         # WebDriverWait(driver, 10).until(
#         #     EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
#         # )
#         iframes = driver.find_elements(By.TAG_NAME, "iframe")
#         for index, iframe in enumerate(iframes):
#             driver.switch_to.frame(iframe)
#             # Check if the desired element is in this iframe
#             if driver.find_elements(By.CSS_SELECTOR, "div.popup_inner"):
#                 break  # Found the right iframe
#             driver.switch_to.default_content()  
        
        
#         driver.save_screenshot('./iframe.png')
        
#         html_content = driver.page_source
#         # return html_content
        
#         # order_button = WebDriverWait(driver, 10).until(
#         #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
#         # )
#         # order_button.click()
        
#         # time.sleep(5)
        
#         # driver.save_screenshot('./order_button.png')
        
#         # # html_content = driver.page_source
#         # # return html_content
        
#         # current_url = driver.current_url
#         # return current_url
        
#         try:
#             order_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
#             )
#             order_button.click()
#         except Exception as e:
#             # If normal click fails, try JavaScript click
#             print(f"Normal click failed: {e}, attempting JavaScript click")
#             driver.execute_script("arguments[0].click();", order_button)

#         time.sleep(5)
#         driver.save_screenshot('./order_button.png')
#         current_url = driver.current_url
#         return current_url

#     except Exception as e:
#         print(f"Error encountered: {str(e)}")
#         return False

#     finally:
#         driver.quit()

        
        
# def complete_order(driver):
#     try:
#         driver.save_screenshot('./modal_appeared1.png')
#         # Wait for the modal to fully appear and ensure all elements are loaded
#         WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popup_inner"))
#         )
#         driver.save_screenshot('./modal_appeared2.png')
#         modal_html = driver.find_element(By.CSS_SELECTOR, "div.popup_inner").get_attribute('innerHTML')
#         return modal_html
        
#         # Find the 'Complete Order' button
#         order_button = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
#         )
        
#         # Scroll the button into view (useful if the modal is large or off screen)
#         ActionChains(driver).move_to_element(order_button).perform()

#         # Check if the button is clickable, and click it
#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup-buy__footer-btn"))
#         )
#         order_button.click()

#         # Wait for the checkout process to initiate, this condition should be specific to your application
#         WebDriverWait(driver, 10).until(
#             lambda driver: "checkout" in driver.current_url
#         )
        
#         current_url = driver.current_url
#         return current_url

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return False

#     finally:
#         driver.quit()