import logging
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


# pipelines.py
class ValidationPipeline:
    """
    Ürün ve yorum verilerinin doğruluğunu kontrol eden pipeline
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if spider.name == 'trendyol_electronics':
            return self._validate_product(adapter, item)
        elif spider.name == 'trendyol_reviews':
            return self._validate_review(adapter, item)
        return item

    def _validate_product(self, adapter, item):
        required_fields = ['name', 'price', 'url']
        for field in required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing {field} in {item}")
        return item

    def _validate_review(self, adapter, item):
        required_fields = ['product_id',
                           'review_date', 'rating', 'review_text']
        for field in required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing {field} in {item}")

        # Rating kontrolü
        rating = adapter.get('rating')
        if rating and (not isinstance(rating, (int, float)) or not 1 <= rating <= 5):
            raise DropItem(f"Invalid rating value: {rating}")

        return item


class DuplicatesPipeline:
    """
    Tekrar eden ürünleri filtreleyen pipeline
    """

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter['url']

        if url in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item}")

        self.urls_seen.add(url)
        return item
