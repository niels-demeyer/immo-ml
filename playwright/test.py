from WebScraper_file import WebScraper
import os

scraper = WebScraper()
# scraper.construct_links_per_province()
# scraper.scrape_provinces()
results = scraper.scrape_individual_house("https://www.immoweb.be/en/classified/house/for-sale/deurle/9831/10884937")
print(results)