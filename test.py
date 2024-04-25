from WebScraper_file import WebScraper
import os

scraper = WebScraper()
provinces = scraper.construct_links_per_province()
print(provinces)