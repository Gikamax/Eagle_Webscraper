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
            for municipality in MUNICIPALITY_AND_PLACE.keys():
                for location in MUNICIPALITY_AND_PLACE[municipality]:
                    _scraper = JobScraper(location, municipality)
                    _scraper.navigate_home_screen()
                    _scraper.prepare_site()
                    _scraper.loop_through_webpages()
            JobScraper.extract_to_csv("C:\\Temp\\")
            break
        elif user_input.lower() == 'jobtitle':
            break
        else:
            print("Please add correct command.")


if __name__ == "__main__":
    main()