from typing import Iterable
import scrapy


class PraktikerSpider(scrapy.Spider):
    name = 'praktiker_spider'

    def start_requests(self):
        # Търсената дума - можеш да я промениш според нуждите
        search_term = "пясък"
        url = f"https://praktiker.bg/bg/search/{search_term}"
        yield scrapy.Request(url=url, callback=self.parse_results)

    def parse_results(self, response):
        # Извличане на продуктите от резултатите
        products = response.css('h2.product-item__title')
        for product in products:
            name = product.css('a::attr(title)').get()
            link = product.css('a::attr(href)').get()

            # Извличане на цената
            price_value = product.xpath(
                '//span[@class="price__value"]/text()').get()
            price_sup = product.xpath('//sup/text()').get()
            price = f"{price_value}.{price_sup} лв"

            yield {
                'name': name,
                'link': response.urljoin(link),
                'price': price,
            }

        # Откриване и следване на линк към следващата страница с резултати (ако има)
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_results)
