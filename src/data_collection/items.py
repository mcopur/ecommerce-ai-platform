from scrapy import Item, Field
from itemloaders.processors import TakeFirst, Join, Identity


class ProductBase(Item):
    """
    Temel ürün sınıfı - tüm ürün tiplerinin temel sınıfı
    """
    name = Field()
    url = Field()
    created_at = Field()
    updated_at = Field()


class ProductItem(ProductBase):
    """
    E-ticaret ürünleri için özelleştirilmiş ürün sınıfı
    """
    name = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    brand = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    url = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    specifications = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
