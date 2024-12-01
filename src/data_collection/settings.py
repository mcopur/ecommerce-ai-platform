"""
Basic Scrapy settings for e-commerce data collection project.
"""
from pathlib import Path

# Project Structure (Mevcut yapıyı koruyoruz)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Basic Configuration (Mevcut yapıyı koruyoruz)
BOT_NAME = 'ecommerce_ai_platform'
SPIDER_MODULES = ['src.data_collection.spiders']
NEWSPIDER_MODULE = 'src.data_collection.spiders'

# Crawling Settings (Mevcut ayarları genişletiyoruz)
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # Yeni eklenen
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True  # Yeni eklenen

# Retry Settings (Yeni eklenen bölüm)
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

# User Agent Settings (Mevcut yapıyı genişletiyoruz)
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'tr,en-US;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Pipeline Settings (Mevcut yapıyı koruyoruz)
ITEM_PIPELINES = {
    'src.data_collection.pipelines.ValidationPipeline': 300,
    'src.data_collection.pipelines.DuplicatesPipeline': 500,
}

# Output Settings (Mevcut yapıyı koruyoruz ve genişletiyoruz)
FEED_FORMAT = 'json'
FEED_URI = str(DATA_DIR / 'products_%(time)s.json')
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_INDENT = 4  # Yeni eklenen - JSON formatlaması için

# Cache Settings (Opsiyonel yeni bölüm)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = str(DATA_DIR / 'httpcache')

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,
    'src.data_collection.middlewares.CustomRobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 300,
}
