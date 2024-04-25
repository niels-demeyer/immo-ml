from playwright import sync_playwright

class WebScraper:
    def __init__(self):
        page = None
        browser = None
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.provinces = ["oost-vlaanderen", "west-vlaanderen", "antwerpen", "limburg", "vlaams-brabant", "brussel", "waals-brabant", "henegouwen", "luik", "luxemburg", "namen"]
    def get_links_per_province(self):
        # Get the links of the houses per provinces
        