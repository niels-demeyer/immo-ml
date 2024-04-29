import hrequests
from bs4 import BeautifulSoup
import json
from selectolax.parser import HTMLParser
import concurrent.futures


class ExtractPage:
    """
    Extracts a json from the page's html where we have all the characteristics of a property.
    Has a method to filter out which page has only one property or multiple listed inside.
    Args:
        url (str): url of a listing in the website.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        try:
            self.raw = self.get_raw_data()
            self.single = self.is_single_listing()
        except ValueError:
            print(f"Error: No script tag found in the HTML for URL {self.url}")
            self.raw = None
            self.single = None

    def get_raw_data(self):
        response = self.make_request()
        if response is not None:
            content = response.content
            html = HTMLParser(content)
            raw_data = self.extract_data_from_script(html)
            if raw_data is not None:
                return json.loads(raw_data)
            else:
                raise ValueError("No script tag found in the HTML.")
        else:
            return None

    def make_request(self):
        while True:
            try:
                return hrequests.get(self.url, headers=self.headers)
            except hrequests.exceptions.ClientException as e:
                print(f"An error occurred while making a request to {self.url}: {e}")
                pass

    def extract_data_from_script(self, html):
        script = html.css_first("script[type='text/javascript']")
        if script:
            return (
                script.text()
                .replace("window.classified = ", "")
                .replace(";", "")
                .strip()
            )
        else:
            print("No script tag found in the HTML.")
            return None

    def is_single_listing(self) -> bool:
        # Uses key "cluster" to filter if multiple or single
        return self.raw and (
            self.raw["cluster"] == "null" or self.raw["cluster"] is None
        )

    def check_and_return_single_listing(self):
        if self.is_single_listing():
            return self.raw
        else:
            return None

    def to_dict(self):
        return {
            "url": self.url,
            "raw": self.raw,
            "single": self.single,
        }