from scrapy import Item, Field
from itemloaders.processors import TakeFirst, Join, Identity
from .processors import TurkishDateProcessor


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


class ReviewBase(Item):
    """
    Temel yorum sınıfı - tüm yorum tiplerinin temel sınıfı
    """
    product_id = Field()  # Yorumun ait olduğu ürün ID'si
    created_at = Field()  # Yorumun oluşturulma tarihi
    updated_at = Field()  # Yorumun güncellenme tarihi


class ReviewItem(ReviewBase):
    """
    E-ticaret yorumları için özelleştirilmiş yorum sınıfı
    """
    reviewer_name = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    review_date = Field(
        input_processor=TurkishDateProcessor,
        output_processor=TakeFirst()
    )
    rating = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    review_text = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    seller = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    likes = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
    photos = Field(
        input_processor=Identity(),  # Fotoğraf URL'leri liste olarak saklanacak
        output_processor=TakeFirst()
    )
    verified_purchase = Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst()
    )
