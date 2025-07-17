# utils.py
import requests
from datetime import date
from .models import CurrencyRate

def fetch_and_save_currency_rates():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    data = response.json()

    for item in data:
        if item["Ccy"] in ["USD", "RUB"]:
            CurrencyRate.objects.update_or_create(
                currency=item["Ccy"],
                date=date.today(),
                defaults={"rate": item["Rate"].replace(",", ".")}
            )

    # UZS сам к себе равен
    CurrencyRate.objects.update_or_create(
        currency="UZS",
        date=date.today(),
        defaults={"rate": 1}
    )





import json
from set_main.models import City, District

def import_from_json(filepath='locations.json'):
    with open(filepath, encoding='utf-8') as f:
        items = json.load(f)

    oblasts = [i for i in items if i['admin_level'] == 4]
    districts = [i for i in items if i['admin_level'] == 6]

    for obl in oblasts:
        City.objects.get_or_create(name=obl['name'])

    city_map = {c.name: c for c in City.objects.all()}
    for d in districts:
        parent_name = next((obl['name'] for obl in oblasts if obl['id'] == d['parent_id']), None)
        if parent_name:
            city = city_map[parent_name]
            District.objects.get_or_create(name=d['name'], city=city)

    print("✅ Импорт завершён")


