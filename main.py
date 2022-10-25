from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

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
    #search_bar_location.send_keys(Keys.RETURN)


def main():
    driver.get(URL)

    navigate_home_screen("Timmerman", "Enschede", driver)

    try:
        jobs_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mosaic-jobcards")))
    except Exception as e:
        print("Element not found")
        driver.quit()
    
    cards = jobs_list.find_elements(By.CLASS_NAME, "job_seen_beacon")
    for card in cards:
        job_title = card.find_element(By.TAG_NAME, "h2")
        company = card.find_element(By.CLASS_NAME, "companyName")
        print(job_title.text)
        print(company.text)
        url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

    next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
    actions = ActionChains(driver)
    actions.move_to_element(next_page_button)
    next_page_button.click()
    time.sleep(5)

    # page_navigation_banner = driver.find_element(By.TAG_NAME, "nav")
    # page_navigation_buttons = page_navigation_banner.find_elements(By.TAG_NAME, 'a')
    # print(len(page_navigation_buttons))
    # next_page_button = page_navigation_buttons[-1]
    # next_page_button.select()
    # page_next = driver.find_element(By.CLASS_NAME, "css-fnfhcj e8ju0x50")
    # print(page_next)
    driver.quit()



if __name__ == "__main__":
    main()