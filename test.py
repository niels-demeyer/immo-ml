from WebScraper_file import WebScraper
import os

scraper = WebScraper()
scraper.construct_links_per_province()
scraper.scrape_provinces()