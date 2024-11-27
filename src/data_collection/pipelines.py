import logging
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """
    Ürün verilerinin doğruluğunu kontrol eden pipeline
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Zorunlu alanların kontrolü
        required_fields = ['name', 'price', 'url']
        for field in required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing {field} in {item}")

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
