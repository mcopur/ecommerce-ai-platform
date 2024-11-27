"""
Enhanced spider implementation for Trendyol electronics data collection.
Includes improved selectors and error handling.
"""
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, Join
import logging

from ..items import ProductItem

logger = logging.getLogger(__name__)


class TrendyolSpider(CrawlSpider):
    name = 'trendyol_electronics'
    allowed_domains = ['trendyol.com']
    start_urls = ['https://www.trendyol.com/cep-telefonu-x-c103498']

    rules = (
        # Ürün detay sayfalarına git
        Rule(
            LinkExtractor(
                allow=r'/.*-p-\d+',  # ürün detay sayfası URL pattern'i
                restrict_xpaths="//div[contains(@class, 'p-card-wrppr')]"
            ),
            callback='parse_product',
            follow=True
        ),
        # Sayfalama için
        Rule(
            LinkExtractor(
                restrict_xpaths="//div[contains(@class, 'pgntn')]//a"
            ),
            follow=True
        ),
    )

    def parse_product(self, response):
        self.logger.debug(f"Processing product page: {response.url}")
        try:
            loader = ItemLoader(item=ProductItem(), response=response)

            # Her adımda debug log ekleyelim
            name = response.xpath(
                '//h1[contains(@class, "pr-new-br")]//span/text()').get()
            self.logger.debug(f"Extracted name: {name}")

            price = response.xpath(
                '//span[contains(@class, "prc-dsc")]/text()').get()
            self.logger.debug(f"Extracted price: {price}")

            brand = response.xpath(
                '//h1[contains(@class, "pr-new-br")]//a/text()').get()
            self.logger.debug(f"Extracted brand: {brand}")

            if name:
                loader.add_value('name', name.strip())
            if price:
                # Fiyat temizleme
                cleaned_price = price.replace('TL', '').strip()
                cleaned_price = cleaned_price.replace(
                    '.', '').replace(',', '.')
                loader.add_value('price', cleaned_price)
            if brand:
                loader.add_value('brand', brand.strip())

            loader.add_value('url', response.url)

            # Ürün özellikleri
            specs = {}
            specs_elements = response.xpath(
                "//ul[contains(@class, 'detail-attr-container')]/li")
            self.logger.debug(
                f"Found {len(specs_elements)} specification elements")

            for spec in specs_elements:
                key = spec.xpath(
                    './/span[contains(@class, "attr-name")]/text()').get()
                value = spec.xpath(
                    './/div[contains(@class, "attr-value-name-w")]/text()').get()
                if key and value:
                    specs[key.strip()] = value.strip()

            loader.add_value('specifications', specs)

            return loader.load_item()

        except Exception as e:
            self.logger.error(
                f"Error parsing product {response.url}: {str(e)}")
            self.logger.exception("Full traceback:")
            return None

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")
