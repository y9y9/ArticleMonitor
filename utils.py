"""Python imports"""
import os
import logging
from time import sleep
from datetime import datetime
import diff_match_patch as dmp_module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions



# SET SELENIUM LOGGING LEVELS TO WARNING
logging.getLogger('selenium').setLevel(logging.WARNING)


# FOR RUNNING IN CHROME
def open_chrome_window():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_changes(old_text: str, new_text: str) -> list[tuple[tuple, tuple]]:
    # DIFF MODULE OBJECT
    dmp = dmp_module.diff_match_patch()

    # GETTING DIFFERENCE BETWEEN THE SEQUENCES
    diff = dmp.diff_main(old_text, new_text)
    dmp.diff_cleanupSemantic(diff)

    # REMOVE UNCHANGED TEXT FROM CONTENT
    def filter_unchanged(content: tuple):
        if content[0] != 0:
            return content

    diff = map(filter_unchanged, diff)
    diff = [change for change in diff if change is not None]

    # GET REMOVALS AND ADDITIONS FROM CONTENTS
    removals = [change for change in diff if change[0] == -1]
    additions = [change for change in diff if change[0] == 1]

    # ZIP REMOVALS AND ADDITIONS AS PAIRS OF CHANGES
    changes = list(zip(removals, additions))

    return changes or None


def start_tracking(driver, original_text) -> None:
    print('-> Monitoring...')
    while True:
        try:
            # CHECK EVERY 10 SECONDS
            sleep(10)

            # CURRENT HTML AND BODY TEXT
            current_html = driver.page_source
            current_text = driver.find_element(By.TAG_NAME, "body").text.strip()

            # COMPARE ORIGINAL AND CURRENT
            changes = get_changes(original_text, current_text)

            # RECORD CHANGES TO FILE IF CHANGES EXIST
            if changes is not None:
                print('-> Changes detected, processing files...')
                # CREATE FILENAME FROM CURRENT TIMESTAMP
                timestamp = datetime.now().strftime("%Y_%m_%d [%H_%M_%S]")

                # CREATE CHANGES DIRECTORY
                os.makedirs('./changes', exist_ok=True)
                filename = os.path.abspath(f"./changes/{timestamp}.txt")

                print("-> Saving changes to file")
                with open(filename, mode='w') as file:
                    # WRITE CHANGES TO NEW FILE
                    for change in changes:
                        old = change[0][1]
                        new = change[1][1]

                        line_number = changes.index(change)+1

                        file.write(f"{line_number}. OLD: {old} NEW: {new}\n")
                
                # SAVE NEW HTML FILE
                print("-> Saving new HTML file")
                with open('new.html', 'w') as file:
                    file.write(current_html)

                print('Done!')
                return

            driver.refresh()
            continue
        
        except KeyboardInterrupt:
            print('\n\nTerminated early by user')
            break
    return


if __name__ == "__main__":
    pass
