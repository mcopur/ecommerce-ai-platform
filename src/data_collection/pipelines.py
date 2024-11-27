"""
Data processing pipelines for scraped items.
"""
import logging
from typing import Dict, Any

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .items import ProductBase

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """Validate scraped items using Pydantic models."""

    def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
        """Validate item data using ProductBase model."""
        try:
            adapter = ItemAdapter(item)
            product_data = dict(adapter)

            # Validate using Pydantic model
            validated_data = ProductBase(**product_data)
            return dict(validated_data)

        except Exception as e:
            logger.error(f"Validation error for item: {str(e)}")
            raise DropItem(f"Invalid item data: {str(e)}")


class DuplicatesPipeline:
    """Remove duplicate items based on URL."""

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
        """Check for duplicate URLs and drop if found."""
        adapter = ItemAdapter(item)
        url = adapter.get('url')

        if url in self.urls_seen:
            raise DropItem(f"Duplicate item found: {url}")

        self.urls_seen.add(url)
        return item
