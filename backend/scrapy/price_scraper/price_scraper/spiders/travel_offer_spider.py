
from datetime import datetime
import scrapy
import sys
import os
import django

# Абсолютен път до Django settings.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.products.models import TravelOffer


class TravelOfferSpider(scrapy.Spider):
    name = 'travel_offer'
    allowed_domains = ['2mko.com']
    start_urls = ['https://www.2mko.com/pochivka-dominikana']

    def parse(self, response):
        title = response.css('h1::text').get().strip()
        departure_date = datetime.strptime('26.12.2025', '%d.%m.%Y').date()
        price_bgn = 5809.00
        price_eur = 2970.00
        phone_numbers = '02 988 38 67, 02 980 29 56, 0885/355 987'

        # Примерна програма — ще я заменим с динамично извличане
        itinerary = """
        1 ДЕН – Полет София – Мадрид с “Wizz Air”. Нощувка в Мадрид.
        2 ДЕН – Полет Мадрид – Пунта Кана с “Iberojet”. Вечеря. Нощувка.
        3 ДЕН – Свободен ден за плаж. AI изхранване.
        """

        TravelOffer.objects.create(
            title=title,
            destination='Пунта Кана',
            transport='Самолет',
            duration_days=10,
            duration_nights=8,
            departure_date=departure_date,
            price_bgn=price_bgn,
            price_eur=price_eur,
            phone_numbers=phone_numbers,
            itinerary=itinerary
        )
