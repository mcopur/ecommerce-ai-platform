"""
Item definitions for product data collection and validation.
"""
from typing import Dict, List, Optional
from datetime import datetime

import scrapy
from pydantic import BaseModel
from itemloaders.processors import TakeFirst, Join, MapCompose


class ProductBase(BaseModel):
    """Base model for product data validation."""
    name: str
    price: float
    brand: str
    url: Optional[str] = None


class ProductItem(scrapy.Item):
    """Scrapy item for product data collection."""
    name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(
            lambda x: x.replace('TL', '').strip().replace(',', '.'),
            float
        ),
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
