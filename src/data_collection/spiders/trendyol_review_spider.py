# src/data_collection/spiders/trendyol_review_spider.py

import scrapy
import json
import logging
from datetime import datetime
from scrapy.exceptions import CloseSpider
from itemloaders import ItemLoader
from ..items import ReviewItem

logger = logging.getLogger(__name__)


class TrendyolReviewSpider(scrapy.Spider):
    name = 'trendyol_reviews'
    allowed_domains = ['trendyol.com', 'apigw.trendyol.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'FEEDS': {
            'reviews_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            }
        },
        'DEFAULT_REQUEST_HEADERS': {
            'accept': '*/*',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.trendyol.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'ty-web-client-async-mode': 'true',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
    }

    def start_requests(self):
        """Yorum sayfası için API isteği oluşturur."""
        try:
            # URL'i parçalara ayır
            # Örnek: https://www.trendyol.com/apple/iphone-13-128-gb.../p-150058735
            url_parts = self.product_url.split('/')

            # Markayı al (apple)
            brand = url_parts[3]

            # Ürün ID'sini içeren son parçayı al
            last_part = url_parts[-1]  # "iphone-13-...-p-150058735"

            # Son parçadan ürün ID'sini ayır
            product_parts = last_part.split('-p-')
            product_id = product_parts[-1]  # "150058735"

            # Ürün adını oluştur
            # URL'den marka ve p- kısmını çıkarıp geriye kalan tüm parçaları al
            product_title = '/'.join(url_parts[4:-1])  # Önceki parçalar
            if len(product_parts) > 1:
                # Son parçanın -p- öncesi
                product_title = f"{product_title}/{product_parts[0]}"

            self.logger.debug(f"Marka: {brand}")
            self.logger.debug(f"Ürün başlığı: {product_title}")
            self.logger.debug(f"Ürün ID: {product_id}")

            # API URL'ini oluştur
            api_url = (
                f"https://apigw.trendyol.com/discovery-web-socialgw-service/reviews"
                f"/{brand}/{product_title}/yorumlar/"
            )

            # Query parametreleri
            params = {
                'culture': 'tr-TR',
                'storefrontId': '1',
                'RRsocialproofAbTesting': 'B',
                'logged-in': 'false',
                'isBuyer': 'false',
                'channelId': '1'
            }

            query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
            api_url = f"{api_url}?{query_string}"

            self.logger.info(f"API isteği başlatılıyor: {api_url}")
        except Exception as e:
            self.logger.error(f"URL işlenirken hata: {str(e)}", exc_info=True)
            raise CloseSpider('URL işleme hatası')

    def parse_reviews(self, response):
        """API yanıtını işler ve yorumları çıkarır."""
        if response.status != 200:
            self.logger.error(
                f"API isteği başarısız. Status: {response.status}")
            self.logger.debug(f"Yanıt başlıkları: {response.headers}")
            self.logger.debug(f"Yanıt içeriği: {response.text[:1000]}...")
            return

        try:
            data = json.loads(response.text)
            self.logger.debug(
                f"API yanıtı: {json.dumps(data, indent=2)[:1000]}...")

            reviews = data.get('result', {}).get(
                'ratingAndReviewResponse', {}).get('reviews', [])
            self.logger.info(f"Bulunan yorum sayısı: {len(reviews)}")

            for review in reviews:
                try:
                    loader = ItemLoader(item=ReviewItem())

                    loader.add_value('product_id', response.meta['product_id'])
                    loader.add_value(
                        'reviewer_name', review.get('userFullName'))
                    loader.add_value(
                        'review_date', review.get('commentDateISOtype'))
                    loader.add_value('rating', review.get('rate'))
                    loader.add_value('review_text', review.get('comment'))
                    loader.add_value('seller', review.get('sellerName'))
                    loader.add_value('likes', review.get('reviewLikeCount', 0))

                    # Fotoğrafları işle
                    if 'mediaFiles' in review:
                        photos = [img.get('url')
                                  for img in review.get('mediaFiles', [])]
                        loader.add_value('photos', photos)

                    yield loader.load_item()

                except Exception as e:
                    self.logger.error(
                        f"Yorum işlenirken hata: {str(e)}", exc_info=True)
                    continue

            # Sayfalama bilgilerini al
            paging_data = (
                data.get('result', {})
                .get('ratingAndReviewResponse', {})
                .get('pagingData', {})
            )
            current_page = paging_data.get('page', 0)
            total_pages = paging_data.get('totalPages', 0)

            # Sonraki sayfa için istek oluştur
            if self.should_follow_next_page(current_page, total_pages):
                next_url = response.url.replace(
                    f'page={current_page}',
                    f'page={current_page + 1}'
                )

                self.logger.info(f"Sonraki sayfa: {next_url}")

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_reviews,
                    errback=self.handle_error,
                    meta=response.meta,
                    dont_filter=True
                )

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse hatası: {str(e)}")
            self.logger.debug(f"Yanıt içeriği: {response.text[:1000]}...")
        except Exception as e:
            self.logger.error(
                f"API yanıtı işlenirken hata: {str(e)}", exc_info=True)

    def should_follow_next_page(self, current_page, total_pages):
        """Sonraki sayfaya geçilip geçilmeyeceğini kontrol eder."""
        # Maksimum sayfa kontrolü
        if self.max_pages and self.processed_pages >= self.max_pages:
            self.logger.info(
                f"Maksimum sayfa sayısına ulaşıldı: {self.max_pages}")
            return False

        return current_page < total_pages - 1

    def handle_error(self, failure):
        """Hata durumlarını yönetir ve loglar."""
        self.logger.error(f"Request hatası: {failure.type.__name__}")
        self.logger.error(f"Hata detayı: {str(failure.value)}")

        self.crawler.stats.inc_value(f'error_count/{failure.type.__name__}')
