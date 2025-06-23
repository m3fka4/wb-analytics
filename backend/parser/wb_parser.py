#!/usr/bin/env python3
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ——— Указываем Django-проект
# 1) путь до папки frontend (там, где manage.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
sys.path.insert(0, BASE_DIR)

# 2) настраиваем окружение Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')
import django
django.setup()

# теперь можно импортировать Django-модель
from analytics.models import Product

# Опционально: читаем .env из корня бэкенда, если там лежат нужные ключи (например для прокси или API-ключей)
BE_ENV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(BE_ENV):
    load_dotenv(BE_ENV)

def parse_wb(query: str, max_pages: int = 1):
    """
    Парсит Wildberries по JSON-API, сохраняет товары в Django-модель Product.
    """
    api_url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    for page in range(1, max_pages + 1):
        params = {
            "appType": 1,
            "curr": "rub",
            "lang": "ru",
            "locale": "ru",
            "query": query,
            "resultset": "catalog",
            "dest": -1257786,  # обязательный параметр
            "sort": "popular",
            "page": page,
        }
        try:
            resp = requests.get(api_url, params=params, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] Страница {page}: {e}")
            continue

        data = resp.json().get("data", {})
        products = data.get("products", [])
        if not products:
            print(f"[INFO] Страница {page}: товаров не найдено")
            break

        for p in products:
            try:
                name = p.get("name", "").strip()
                price = p.get("priceU", 0) / 100
                sale_u = p.get("salePriceU")
                discounted = (sale_u / 100) if sale_u is not None else None
                rating = p.get("rating")
                reviews = p.get("feedbacks")

                # создаём или обновляем (по уникальному имени)
                obj, created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        "price": price,
                        "discounted_price": discounted,
                        "rating": rating,
                        "reviews_count": reviews,
                    }
                )
                print(f"{'Создано' if created else 'Обновлено'}: {name}")
            except Exception as e:
                print(f"[ERROR] Сохранение товара '{name}': {e}")

        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python wb_parser.py <запрос> [макс_страниц]")
        sys.exit(1)

    q = sys.argv[1]
    pages = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    parse_wb(q, pages)