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

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    rules = (
        # Ürün detay sayfalarına git
        Rule(
            LinkExtractor(
                restrict_xpaths="//div[contains(@class, 'p-card-wrppr')]",
                deny=('/sr', '/sr?', '/favori')
            ),
            callback='parse_product',
            follow=True
        ),
        # Sayfalama
        Rule(
            LinkExtractor(
                restrict_xpaths="//div[contains(@class, 'pgntn')]//a"
            ),
            follow=True
        ),
    )

    def parse_product(self, response):
        """
        Ürün detay sayfasından veri çek.
        """
        try:
            loader = ItemLoader(item=ProductItem(), response=response)

            # Temel ürün bilgileri
            loader.add_xpath('name', "//h1[@class='pr-new-br']/text()")
            loader.add_xpath(
                'price', "//div[contains(@class, 'pr-bx-w')]//span[@class='prc-dsc']/text()")
            loader.add_xpath(
                'brand', "//div[contains(@class, 'pr-bx-w')]//a[@class='br-nm']/text()")
            loader.add_value('url', response.url)

            # Log başarılı parse
            logger.info(f"Successfully parsed product: {response.url}")

            return loader.load_item()

        except Exception as e:
            logger.error(f"Error parsing product {response.url}: {str(e)}")
            return None

    def closed(self, reason):
        """
        Spider kapandığında istatistikleri logla.
        """
        stats = self.crawler.stats.get_stats()
        logger.info(f"Spider closed: {reason}")
        logger.info(
            f"Total items scraped: {stats.get('item_scraped_count', 0)}")
        logger.info(
            f"Total pages crawled: {stats.get('response_received_count', 0)}")
