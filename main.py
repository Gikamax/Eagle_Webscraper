from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pandas as pd # Use Dataframe as main storage and export in Class. 

PATH = "C:\Program Files (x86)\chromedriver.exe"
URL = "https://nl.indeed.com/"

driver = webdriver.Chrome(PATH)

def navigate_home_screen(function:str, location:str, driver:webdriver=driver):
    # Locating Searchbars
    search_bar_function = driver.find_element(By.ID, "text-input-what")
    search_bar_location = driver.find_element(By.ID, "text-input-where")
    
    # Filling searchbars
    search_bar_function.send_keys(function)
    search_bar_location.send_keys(location)
    driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton").click()


def main():
    driver.get(URL)

    navigate_home_screen("Timmerman", "Enschede", driver)

    # Create second tab for details of job
    driver.execute_script("window.open('');")
    # Create Actions for moving down screen
    actions = ActionChains(driver)

    try:
        jobs_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mosaic-jobcards")))
    except Exception as e:
        print("Element not found")
        driver.quit()
    

    # Delete Cookies
    reject_all_cookies = driver.find_element(By.ID, "onetrust-reject-all-handler")
    reject_all_cookies.click()

    # Reject Google Login
    reject_google_login = driver.find_element(By.XPATH, "//button[@class='icl-CloseButton icl-Card-close']")
    reject_google_login.click()

    while True:
        try: # Try block for Pop-Up windows
            cards = jobs_list.find_elements(By.CLASS_NAME, "job_seen_beacon")
            for card in cards:
                job_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                # switch to Second Tab 
                driver.switch_to.window(driver.window_handles[1])
                # Insert job_url 
                driver.get(job_url)

                # Jobpage scrapping
                job_title = driver.find_element(By.TAG_NAME, "h1")
                print(job_title.text)

                organization = driver.find_element(By.XPATH, "//div[@class='jobsearch-InlineCompanyRating-companyHeader']/a")
                print(organization.text)
                location = driver.find_element(By.XPATH, "//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div[2]/div")
                print(location.text)
                try: # original Vacancy not always present
                    link_to_original_vacancy = driver.find_element(By.XPATH, "//div[@id='originalJobLinkContainer']/a").get_attribute('href')
                except:
                    link_to_original_vacancy = "No original vacancy link found."
                print(link_to_original_vacancy)

                time.sleep(2)
                # Switch back to main
                driver.switch_to.window(driver.window_handles[0])

            try:
                next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
            except Exception as e:
                break
            actions.move_to_element(next_page_button)
            next_page_button.click()
        
        except ElementClickInterceptedException: # Error given by Selenium 
            close_pop_up_window_button = driver.find_element(By.XPATH, "//button[@class'icl-CloseButton icl-Modal-close']")
            close_pop_up_window_button.click()
            pass

        except Exception as e:
            print(e)
    time.sleep(5)

    driver.quit()



if __name__ == "__main__":
    main()