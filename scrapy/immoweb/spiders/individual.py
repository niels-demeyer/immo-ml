import scrapy
from scrapy.selector import Selector

class IndividualSpider(scrapy.Spider):
    name = "individual"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/classified/house/for-sale/sint-martens-latem/9830/11238297"]

    def parse(self, response):
        # Get the details of the house
        house_details = {}
        # Find all tables
        tables = Selector(response).xpath('//table[@class="classified-table"]')
        for table in tables:
            # Iterate over the rows in the table
            rows = table.xpath('.//tr')
            for row in rows:
                # Get the key from the th element
                key = row.xpath('.//th/text()').get()
                # Check if the td element contains an a element
                if row.xpath('.//td/a'):
                    # If it does, get the href attribute and the text
                    value = {
                        'href': row.xpath('.//td/a/@href').get(),
                        'text': row.xpath('.//td/a/text()').get()
                    }
                elif row.xpath('.//td/span[@class="sr-only"]'):
                    # If the td element contains a span with class sr-only, get the text from this span
                    value = row.xpath('.//td/span[@class="sr-only"]/text()').get()
                else:
                    # Otherwise, get the text from the td element
                    value = row.xpath('.//td/text()').get()
                if key and value:
                    # If both key and value were found, add them to the dictionary
                    house_details[key.strip()] = value.strip()

        # Extract the entire address as a single string
        address = response.xpath('//button[contains(@class, "classified__information--address-map-button")]/text()').getall()
        house_details['address_home'] = ' '.join(address).strip()

        yield house_details