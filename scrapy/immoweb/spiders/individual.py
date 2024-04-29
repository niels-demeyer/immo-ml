import scrapy


class IndividualSpider(scrapy.Spider):
    name = "individual"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en"]

    def parse(self, response):
        pass
