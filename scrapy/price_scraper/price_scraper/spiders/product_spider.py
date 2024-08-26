import scrapy


class ProductSpiderSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["praktiker.bg"]
    start_urls = ["https://praktiker.bg/bg/Stroitelni-materiali/c/P1302"]

    def parse(self, response):
        pass
