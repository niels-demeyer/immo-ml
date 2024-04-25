from playwright.sync_api import sync_playwright

class WebScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.provinces = ["oost-vlaanderen", "west-vlaanderen", "antwerpen", "limburg", "vlaams-brabant", "brussel", "waals-brabant", "henegouwen", "luik", "luxemburg", "namen"]
        self.provinces_links = {}

    def construct_links_per_province(self):
        # Get the links of the houses per provinces
        for i in self.provinces:
            url = f"https://www.immoweb.be/en/search/house/for-sale/{i}/province?countries=BE&page=1&orderBy=relevance"
            self.provinces_links[i] = url
        return self.provinces_links