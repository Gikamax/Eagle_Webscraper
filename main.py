from municipality_and_place import MUNICIPALITY_AND_PLACE
from scraper import JobScraper, helper_functions


def main():
    helper_functions.display_banner()
    while True:
        helper_functions.display_introduction_text()
        user_input = input("What do you want to do? ")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'find all':

            # Printing Process
            print("Starting Finding All Vacancies.")

            for municipality in MUNICIPALITY_AND_PLACE.keys():
                for location in MUNICIPALITY_AND_PLACE[municipality]:
                    print(f"Finding Vacancies for {municipality}: {location}.")
                    _scraper = JobScraper(location, municipality)
                    _scraper.navigate_home_screen()
                    _scraper.prepare_site()
                    _scraper.loop_through_webpages()

            print("Extracting to CSV.")
            JobScraper.extract_to_csv()
            break

        # specific JobTitle
        elif user_input.lower() == 'jobtitle':
            job_input = input(
                "What job would you like to search for? (Spaces are accepted) ")

            # Printing Process
            print(f"Starting Finding Vacancies for job {job_input}.")

            for municipality in MUNICIPALITY_AND_PLACE.keys():
                for location in MUNICIPALITY_AND_PLACE[municipality]:
                    print(
                        f"Finding Vacancies for {job_input} in {municipality}: {location}")
                    _jobscraper = JobScraper(location, municipality, job_input)
                    _jobscraper.navigate_home_screen()
                    _jobscraper.prepare_site()
                    _jobscraper.loop_through_webpages()

            print("Extracting to CSV.")
            JobScraper.extract_to_csv()
            break

        else:
            print("Please add correct command.")


if __name__ == "__main__":
    main()
