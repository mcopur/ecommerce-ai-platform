"""
Basic Scrapy settings for e-commerce data collection project.
"""
from pathlib import Path

# Project Structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Basic Configuration
BOT_NAME = 'ecommerce_ai_platform'
SPIDER_MODULES = ['src.data_collection.spiders']
NEWSPIDER_MODULE = 'src.data_collection.spiders'

# Crawling Settings
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 2

# Enable or disable user agent rotation
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Configure item pipelines
ITEM_PIPELINES = {
    'src.data_collection.pipelines.ValidationPipeline': 300,
    'src.data_collection.pipelines.DuplicatesPipeline': 500,
}

# Output Settings
FEED_FORMAT = 'json'
FEED_URI = str(DATA_DIR / 'products_%(time)s.json')
FEED_EXPORT_ENCODING = 'utf-8'
