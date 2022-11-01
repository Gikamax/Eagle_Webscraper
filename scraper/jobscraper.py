import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd

BASE_FILE_PATH = os.getcwd()

# Set up Logging
logging.basicConfig(
    filename=os.path.join(BASE_FILE_PATH, "Webscraper.log"),
    format="%(asctime)s-%(levelname)s-%(message)s"
)

logger = logging.getLogger("Webscraper")
logger.setLevel(logging.INFO)

# Set up Options.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


class JobScraper:
    URL = "https://nl.indeed.com/"
    radius_query = "&radius=0"
    df_result = pd.DataFrame(
        columns=["Functie", "Organisatie", "Plaats", "Gemeente", "URL"])

    @classmethod
    def extract_to_csv(cls) -> None:
        """ Classmethod to extract all retrieved data to csv."""
        JobScraper.df_result.drop_duplicates(
            subset=["Functie", "Organisatie", "Plaats"], inplace=True)
        JobScraper.df_result.to_csv(os.path.join(
            BASE_FILE_PATH, "Jobscraper_results.csv"))

    def __init__(self, location: str, municipality: str, job: str = None):
        self.location = location
        self.municipality = municipality
        self.job = job
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)
        self.actions = ActionChains(self.driver)
        self._data = pd.DataFrame(
            columns=["Functie", "Organisatie", "Plaats", "Gemeente", "URL"])
        logger.info(
            f"Created for Location: '{self.location}'| Municipality: '{self.municipality}'| Mode: '{'Find All' if self.job == None else 'Single Job'}'")

    def reject_all_cookies(self) -> None:
        """Finds cookie pop-up and closes it on the Indeed Search Page."""
        try:
            reject_all_cookies = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler")))
            reject_all_cookies.click()
            logger.info(f"Succesfully rejected Cookies")
        except Exception as e:
            logger.warning(f"Unable to reject cookies due to: {e}")

    def reject_google_login(self) -> None:
        """Finds Google Login pop-up and closes it on the Indeed Search Page."""
        try:
            reject_google_login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@class='icl-CloseButton icl-Card-close']")))
            reject_google_login.click()
            logger.info(f"Succesfully rejected Google Login")
        except Exception as e:
            logger.warning(f"Unable to reject Google Login due to: {e}")

    def switch_to_main_tab(self) -> None:
        """Method to switch to Main-search tab."""
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_second_tab(self) -> None:
        """Method to switch to second opened tab."""
        self.driver.switch_to.window(self.driver.window_handles[1])

    def create_second_tab(self) -> None:
        """Method to create second tab."""
        self.driver.execute_script("window.open('');")
        logger.info(f"Created Second tab.")

    def format_url(self, url: str) -> str:
        """Formats the url with business rules"""
        # Format Location
        location_without_spaces = self.location.replace(
            " ", "+")  # Replace spaces in Placenames with +
        end_of_normal_url_index = url.find(
            location_without_spaces) + len(location_without_spaces)  # Find End of Index
        # Create new url based on new Radius
        url_with_radius = url[:end_of_normal_url_index] + \
            JobScraper.radius_query
        return url_with_radius

    def navigate_home_screen(self) -> None:
        """
        Method to fill in values in Indeed Home page. 
        If provided set Job and Location. After initial load also sets Radius to 0. 
        """
        # Navigate to home screen
        self.driver.get(JobScraper.URL)
        logger.info(f"Opened Indeed Homepage.")
        if self.job != None:
            # Locate SearchBar for Function
            search_bar_function = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "text-input-what")))
            # Input Function
            search_bar_function.send_keys(self.job)
            logger.info(f"Located the job searchbar and filled in {self.job}.")

        # Always need to fill in location
        # Locating Searchbar Location
        search_bar_location = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "text-input-where")))
        # Filling searchbar Location
        search_bar_location.send_keys(self.location)
        logger.info(
            f"Located the location searchbar and filled in {self.location}.")
        # Hitting Search button.
        self.driver.find_element(
            By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton").click()
        logger.info(f"Hit the search button.")

        # Set Radius to 0 KM
        url_with_radius = self.format_url(self.driver.current_url)
        logger.info(f"Formatted the url to: {url_with_radius}")
        self.driver.get(url_with_radius)
        logger.info(f"Inserted the url with radius to webdriver.")

    def prepare_site(self):
        """Clears Cookies, Google Login and creates a second tab and switches back to main tab."""
        self.reject_all_cookies()
        self.reject_google_login()
        self.create_second_tab()
        self.switch_to_main_tab()

    def jobpage_scraping(self, vacancy_url: str) -> pd.DataFrame:
        """Method to retrieve information from the vacancy. """
        # switch to Second Tab
        self.switch_to_second_tab()
        # Insert vacancy url in Second Tab
        self.driver.get(vacancy_url)
        logger.info(f"Begin scrapping {vacancy_url}")

        # Scrape Necessary info
        try:
            job_title = self.driver.find_element(By.TAG_NAME, "h1").text
            logger.info(f"Succesfully scraped Job Title: {job_title}")
        except Exception as e:
            logger.warning(
                f"Unable to find Job Title, because of Exception: {e}.")
            job_title = ""
        try:
            organization = self.driver.find_element(
                By.XPATH, "//div[@class='jobsearch-InlineCompanyRating-companyHeader']/a").text
            logger.info(f"Succesfully scraped Organization: {organization}")
        except:
            logger.warning(
                f"Unable to find Organization, because of Exception: {e}.")
            organization = ""

        try:
            location = self.driver.find_element(
                By.XPATH, "//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div[2]/div").text
            logger.info(f"Succesfully found location: {location}")
        except Exception as e:
            logger.warning(
                f"Unable to find Location, because of Exception: {e}.")
            location = ""
        try:  # original Vacancy not always present
            link_to_original_vacancy = self.driver.find_element(
                By.XPATH, "//div[@id='originalJobLinkContainer']/a").get_attribute('href')
            logger.info(f"Succesfully found Orginal Url.")
        except Exception as e:
            logger.warning(
                f"Unable to find Original url, because of Exception: {e}.")
            link_to_original_vacancy = ""
        # Switch back to main
        self.switch_to_main_tab()
        return pd.DataFrame({'Functie': job_title, "Organisatie": organization, "Plaats": location, "Gemeente": self.municipality, "URL": link_to_original_vacancy}, index=[0])

    def loop_through_webpages(self):
        """Method to Loop through all pages with vacancies."""
        while True:
            try:
                jobs_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "mosaic-jobcards")))
                logger.info(f"Found element Jobs List.")
                cards = jobs_list.find_elements(
                    By.CLASS_NAME, "job_seen_beacon")
                for card in cards:
                    try:
                        vacancy_url = card.find_element(
                            By.TAG_NAME, 'a').get_attribute('href')
                        self._data = pd.concat(
                            [self._data, self.jobpage_scraping(vacancy_url)], ignore_index=True)
                        logger.info(f"Found and scraped {vacancy_url}.")
                    except Exception as e:
                        logger.warning(f"Url not found, because {e}.")

                try:
                    next_page_button = self.driver.find_element(
                        By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
                    self.actions.move_to_element(next_page_button)
                    next_page_button.click()
                    logger.info(f"Switched to next page.")
                except Exception as e:
                    break

            except ElementClickInterceptedException:  # Error given by Selenium
                close_pop_up_window_button = self.driver.find_element(
                    By.XPATH, "//button[@class'icl-CloseButton icl-Modal-close']")
                close_pop_up_window_button.click()

            except Exception as e:
                logger.warning(f"Loop interrupted because {e}.")

        JobScraper.df_result = pd.concat(
            [JobScraper.df_result, self._data], ignore_index=True)
        logger.info("Finished run.")
        self.driver.quit()

    def jobs_to_csv(self):
        """Method to extract information to csv."""
        self._data.drop_duplicates(inplace=True)
        self._data.to_csv(os.path.join(os.getcwd(), f"{self.job}_data.csv"))
