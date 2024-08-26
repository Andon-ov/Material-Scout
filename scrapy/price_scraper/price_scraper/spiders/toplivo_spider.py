import scrapy


class ToplivoSpider(scrapy.Spider):
    name = "toplivo_spider"

    def start_requests(self):
        search_term = "пясък"
        # URL на търсенето
        url = f"https://toplivo.bg/rezultati-ot-tarsene/{search_term}"
        yield scrapy.Request(url=url, callback=self.parse_results)

    def parse_results(self, response):
        # Извличане на продуктите от резултатите
        products = response.css('div.productWapper1.search')
        for product in products:

            name = product.css('span.model::text').get()

            price = product.css('div.cena span.beforedot::text').get()

            link = product.css('a::attr(href)').get()

            yield {
                'name': name,
                'price': price,
                'link': response.urljoin(link),
            }

        # Откриване и следване на линк към следващата страница с резултати (ако има)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_results)


# run with "scrapy crawl toplivo_spider -o toplivo_products.json"