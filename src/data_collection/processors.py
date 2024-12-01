import logging
from datetime import datetime
from itemloaders.processors import MapCompose

logger = logging.getLogger(__name__)


def turkish_date_processor(value):
    """
    Türkçe tarih formatını ISO formatına dönüştüren processor fonksiyonu.
    Örnek: '24 Kasım 2024' -> '2024-11-24'

    Args:
        value (str): Dönüştürülecek tarih string'i

    Returns:
        str: ISO formatında tarih string'i veya None (hata durumunda)
    """
    MONTH_MAP = {
        'Ocak': '01', 'Şubat': '02', 'Mart': '03', 'Nisan': '04',
        'Mayıs': '05', 'Haziran': '06', 'Temmuz': '07', 'Ağustos': '08',
        'Eylül': '09', 'Ekim': '10', 'Kasım': '11', 'Aralık': '12'
    }

    if not value:
        return None

    try:
        day, month, year = value.strip().split()
        month = MONTH_MAP[month]
        return f"{year}-{month}-{day.zfill(2)}"
    except (ValueError, KeyError) as e:
        logger.error(f"Date parsing error: {str(e)} for value: {value}")
        return None


# Processors'ı MapCompose ile oluştur
TurkishDateProcessor = MapCompose(turkish_date_processor)
