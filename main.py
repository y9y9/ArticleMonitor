"""Python imports"""
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException, 
    NoSuchWindowException
)

"""Local imports"""
from utils import (
    open_chrome_window,
    start_tracking
)



if __name__ == "__main__":
    # Create files directory
  #  os.makedirs('./files', exist_ok=True)
  #  os.makedirs('./files/changes', exist_ok=True)

    url = input("Enter article URL:")
    print('\n** PRESS CTRL+C TO TERMINATE **')
    print('-------------------------------')
    
    # CREATE THE WEB DRIVER INSTANCE
    driver = open_chrome_window()

    try:
        # LAUNCH ARTICLE PAGE
        driver.get(url)

        # ORIGINAL HTML CONTENT
        original_html = driver.page_source
        original_text = driver.find_element(By.TAG_NAME, "body").text.strip()
    
        # SAVE ORIGINAL HTML CONTENT
        with open('original.html', 'w', encoding='utf-8') as file:
            file.write(original_html)

        # START TRACKING CHANGES
        start_tracking(driver, original_text)

    except NoSuchWindowException:
        print("The web driver window was closed.")
    
    except WebDriverException as e:
        err_message = ''.join(e.msg.split('(')).split(':')[3]
        message = err_message.split('\n')[0]
        print(f"A web driver error has occcured: {message}")

    finally:
        # FINALLY QUIT DRIVER AND RELEASE RESOURCES
        print('Quitting driver')
        driver.quit()
