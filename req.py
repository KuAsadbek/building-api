import requests
import time
import json

BASE_URL = 'https://nominatim.openstreetmap.org/search'

HEADERS = {'User-Agent': 'StayGlobalParser/1.0'}

def sleep(ms):
    time.sleep(ms / 1000)

def fetch_admin(parent_name, parent_id, admin_level):
    """
    Поиск административных единиц по названию и уровню.
    """
    sleep(2000)  # пауза между запросами
    print(f"\n🔍 Fetching level {admin_level} for: {parent_name}")

    response = requests.get(BASE_URL, params={
        'q': parent_name,
        'format': 'json',
        'addressdetails': 1,
        'limit': 10
    }, headers=HEADERS)

    response.raise_for_status()
    data = response.json()

    result = []
    idx = parent_id * 1000 + admin_level

    for item in data:
        if item.get('class') == 'boundary' and item.get('type') == 'administrative':
            address = item.get('address', {})
            level = address.get('admin_level') or item.get('extratags', {}).get('admin_level')

            if str(level) == str(admin_level):
                name = item['display_name'].split(',')[0].strip()
                idx += 1
                result.append({
                    'id': idx,
                    'name': name,
                    'admin_level': int(admin_level),
                    'parent_id': parent_id,
                    'lat': item['lat'],
                    'lon': item['lon']
                })
                print(f"→ Level {admin_level}: {name}")
    return result

def run(parser_file='locations.json'):
    print("📦 Starting location collection for Uzbekistan")

    # Получаем страну
    r = requests.get(BASE_URL, params={'q': 'Uzbekistan', 'format': 'json', 'limit': 1}, headers=HEADERS)
    r.raise_for_status()
    c = r.json()[0]

    country = {
        'id': 1,
        'name': 'Oʻzbekiston',
        'admin_level': 2,
        'parent_id': None,
        'lat': c['lat'],
        'lon': c['lon']
    }

    print(f"\n🌍 Country: {country['name']}")

    # Получаем области
    oblasts = fetch_admin("Uzbekistan", 1, admin_level=4)

    # Получаем районы для каждой области
    districts = []
    for obl in oblasts:
        districts += fetch_admin(obl['name'], obl['id'], admin_level=6)

    # Объединяем и сохраняем
    data = [country] + oblasts + districts
    with open(parser_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Готово. Сохранено в файл {parser_file}")

if __name__ == '__main__':
    run()
