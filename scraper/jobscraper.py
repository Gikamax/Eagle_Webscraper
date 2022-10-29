from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd


class JobScraper:
    URL = "https://nl.indeed.com/"
    radius_query = "&radius=0"
    df_result = pd.DataFrame(columns=["Functie", "Organisatie", "Plaats", "Gemeente", "URL"])
    
    @classmethod
    def extract_to_csv(cls, destination_path):
        """ Classmethod to extract all retrieved data to csv."""
        JobScraper.df_result.drop_duplicates(inplace=True)
        JobScraper.df_result.to_csv(destination_path + "Jobscraper_results.csv")

    def __init__(self, location:str, municipality:str, job:str = None):
        self.location = location
        self.municipality = municipality
        self.job = job
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.actions = ActionChains(self.driver)

        self._data = pd.DataFrame(columns=["Functie", "Organisatie", "Plaats", "Gemeente", "URL"])

    def reject_all_cookies(self):
        """Finds cookie pop-up and closes it on the Indeed Search Page."""
        reject_all_cookies = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler")))
        reject_all_cookies.click()
    
    def reject_google_login(self):
        """Finds Google Login pop-up and closes it on the Indeed Search Page."""
        reject_google_login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='icl-CloseButton icl-Card-close']")))
        reject_google_login.click()

    def switch_to_main_tab(self):
        """Method to switch to Main-search tab."""
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def switch_to_second_tab(self):
        """Method to switch to second opened tab."""
        self.driver.switch_to.window(self.driver.window_handles[1])        
    
    def create_second_tab(self):
        """Method to create second tab."""
        self.driver.execute_script("window.open('');")

    def navigate_home_screen(self):
        """
        Method to fill in values in Indeed Home page. 
        If provided set Job and Location. After initial load also sets Radius to 0. 
        """
        # Navigate to home screen
        self.driver.get(JobScraper.URL)

        if self.job != None:
            # Locate SearchBar
            search_bar_function = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "text-input-what")))
            #search_bar_function = self.driver.find_element(By.ID, "text-input-what")
            # Input Function 
            search_bar_function.send_keys(self.job)
        
        # Always need to fill in location 
        # Locating Searchbar Location    
        search_bar_location = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "text-input-where")))
        #search_bar_location = self.driver.find_element(By.ID, "text-input-where")
        # Filling searchbars
        search_bar_location.send_keys(self.location)
        # Hitting Search button. 
        self.driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton").click()
        # Set Radius to 0 KM
        end_of_normal_url_index = self.driver.current_url.find(self.location) + len(self.location)
        url_with_radius = self.driver.current_url[:end_of_normal_url_index] + JobScraper.radius_query
        self.driver.get(url_with_radius)
    
    def prepare_site(self):
        """Clears Cookies, Google Login and creates a second tab and switches back to main tab."""
        self.reject_all_cookies()
        self.reject_google_login()
        self.create_second_tab()
        self.switch_to_main_tab()        

    def jobpage_scraping(self, vacancy_url:str) -> pd.DataFrame:
        """Method to retrieve information from the vacancy. """
        # switch to Second Tab 
        self.switch_to_second_tab()
        # Insert vacancy url in Second Tab
        self.driver.get(vacancy_url)

        # Scrape Necessary info
        try:
            job_title = self.driver.find_element(By.TAG_NAME, "h1").text
        except:
            job_title = ""
        try:
            organization = self.driver.find_element(By.XPATH, "//div[@class='jobsearch-InlineCompanyRating-companyHeader']/a").text
        except:
            organization = ""
        
        try:
            location = self.driver.find_element(By.XPATH, "//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div[2]/div").text
        except:
            location = ""
        try: # original Vacancy not always present
            link_to_original_vacancy = self.driver.find_element(By.XPATH, "//div[@id='originalJobLinkContainer']/a").get_attribute('href')
        except:
            link_to_original_vacancy = ""
        # Switch back to main
        self.switch_to_main_tab()
        return pd.DataFrame({'Functie': job_title, "Organisatie": organization, "Plaats": location, "Gemeente": self.municipality, "URL": link_to_original_vacancy}, index = [0])
    
    def loop_through_webpages(self):
        """Method to Loop through all pages with vacancies."""
        while True:
            try:
                jobs_list = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "mosaic-jobcards")))

                cards = jobs_list.find_elements(By.CLASS_NAME, "job_seen_beacon")
                for card in cards:
                    try:
                        vacancy_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        self._data = pd.concat([self._data, self.jobpage_scraping(vacancy_url)], ignore_index=True)
                    except:
                        print("URL not found")

                try:
                    next_page_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
                    self.actions.move_to_element(next_page_button)
                    next_page_button.click()
                except Exception as e:
                    break


            except ElementClickInterceptedException: # Error given by Selenium 
                close_pop_up_window_button = self.driver.find_element(By.XPATH, "//button[@class'icl-CloseButton icl-Modal-close']")
                close_pop_up_window_button.click()

            except Exception as e:
                print(e)
            
        JobScraper.df_result = pd.concat([JobScraper.df_result, self._data], ignore_index=True)
        self.driver.quit()

    def jobs_to_csv(self, destination_path):
        """Method to extract information to csv."""
        self._data.drop_duplicates(inplace=True)
        self._data.to_csv(destination_path + f"{self.job}_data.csv")