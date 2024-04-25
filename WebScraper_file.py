from playwright.sync_api import sync_playwright
from datetime import datetime
import time
class WebScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.provinces = ["oost-vlaanderen", "west-vlaanderen", "antwerpen", "limburg", "vlaams-brabant", "brussel", "waals-brabant", "henegouwen", "luik", "luxemburg", "namen"]
        self.provinces_links = {}

    def close(self):
        self.browser.close()
        self.playwright.stop()
        
    def construct_links_per_province(self):
        # Get the links of the houses per provinces
        for i in self.provinces:
            url = f"https://www.immoweb.be/en/search/house/for-sale/{i}/province?countries=BE&page=1&orderBy=relevance"
            self.provinces_links[i] = url
        return self.provinces_links
    def go_to_url(self, url):
        self.page.goto(url)
    
    def scrape_provinces(self):
        # Get the links of the houses per provinces
        for province, url in self.provinces_links.items():
            self.go_to_url(url)
            self.accept_cookies()
            # Keep scraping and going to the next page until there are no more pages
            while self.go_next_page():
                self.provinces_links[province] = self.page.url
                time.sleep(3)
                self.get_links()
            self.close()
    def scrape_individual_house(self, url):
        self.go_to_url(url)
        self.accept_cookies()
        # Get the details of the house
        house_details = {}
        # Find all tables
        tables = self.page.query_selector_all('.classified-table')
        for table in tables:
            # Iterate over the rows in the table
            rows = table.query_selector_all('tbody.classified-table__body tr.classified-table__row')
            for row in rows:
                # Get the cells in the row
                cells = row.query_selector_all('td.classified-table__data, th.classified-table__header')
                if len(cells) >= 2:
                    # If the row has at least two cells, add the data to the dictionary
                    key = cells[0].inner_text().strip()
                    value = cells[1].inner_text().strip()
                    house_details[key] = value
        return house_details
    
    def accept_cookies(self):
        # Check if the cookies button is present
        cookies_button = self.page.query_selector('button[data-testid="uc-accept-all-button"]')
        if cookies_button:
            # If the button is present, click it
            cookies_button.click()
    def go_next_page(self):
        # Check if the next page link is present
        next_page_link = self.page.query_selector('a.pagination__link--next')
        if next_page_link:
            # If the link is present, get its href attribute and navigate to it
            next_page_url = next_page_link.get_attribute('href')
            self.go_to_url(next_page_url)
            return True  # Return True when the next page link is present
        return False  # Return False when the next page link is not present
    def get_links(self):
        # Get the links of the houses
        houses = self.page.query_selector_all('a.card__title-link')
        links = [house.get_attribute('href') for house in houses]
        print(links)
        return links