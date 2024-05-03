from typing import Iterable
import scrapy
import logging


class MostExpensiveSpider(scrapy.Spider):
    name = "most_expensive"
    allowed_domains = ["www.immoweb.be"]
    start_urls = [
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/east-flanders/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/west-flanders/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/antwerpen/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/limburg/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/vlaams-brabant/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/brussels/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/waals-brabant/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/henegouwen/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/luxembourg/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/namen/province?countries=BE&page=1&orderBy=most_expensive",
        "https://www.immoweb.be/en/search/house-and-apartment/for-sale/luik/province?countries=BE&page=1&orderBy=most_expensive",
    ]

    def parse(self, response):
        found_elements = False
        for h2 in response.css("h2"):
            link = h2.css("a")
            if link:
                href = link.css("::attr(href)").get()
                title = link.css("::text").get()
                if title is not None:
                    title = title.strip()
                yield {
                    "href": href,
                    "title": title,
                }
                found_elements = True
            else:
                logging.info(f"No 'a' tag found in this 'h2' element")

        # If we found elements, yield a request to the next page
        if found_elements:
            next_page_number = response.url.split("=")[-2].split("&")[0]
            next_page_number = int(next_page_number) + 1
            next_page_url = response.url.replace(
                f"page={next_page_number - 1}", f"page={next_page_number}"
            )
            yield scrapy.Request(url=next_page_url, callback=self.parse)
