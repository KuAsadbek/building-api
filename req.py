import requests
import time
import json

COUNTRY = 'Uzbekistan'
BASE_URL = 'https://nominatim.openstreetmap.org/search'
HEADERS = {
    'User-Agent': 'StayGlobalParser/1.0'
}

def sleep(ms):
    time.sleep(ms / 1000)

def fetch_children(lat, lon, parent_id, type_):
    sleep(1000)  # пауза, чтобы не перегружать API
    try:
        params = {
            'q': '',
            'format': 'json',
            'addressdetails': 1,
            'polygon_geojson': 0,
            'extratags': 1,
            'viewbox': f"{float(lon) - 1},{float(lat) - 1},{float(lon) + 1},{float(lat) + 1}",
            'bounded': 1
        }
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        response.raise_for_status()

        data = response.json()

        regions = []
        id_counter = parent_id * 1000  # простой генератор id

        for item in data:
            if (
                item.get('type') == type_ and
                'address' in item and
                ('state' in item['address'] or 'county' in item['address'])
            ):
                name = item['display_name'].split(',')[0]
                region = {
                    'id': id_counter,
                    'name': name,
                    'type': type_,
                    'parent_id': parent_id,
                    'coordinates': {
                        'lat': item['lat'],
                        'lon': item['lon']
                    }
                }
                regions.append(region)
                print(f"Found region: {name}")
                id_counter += 1

        return regions
    except Exception as e:
        print(f"Error fetching children: {e}")
        return []

def fetch_regions(country):
    try:
        params = {
            'q': country,
            'format': 'json',
            'addressdetails': 1,
            'polygon_geojson': 0,
            'limit': 1
        }
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        response.raise_for_status()

        country_data = response.json()[0]
        country_id = 1

        result = [{
            'id': country_id,
            'name': country_data['display_name'],
            'type': 'country',
            'parent_id': None,
            'coordinates': {
                'lat': country_data['lat'],
                'lon': country_data['lon']
            }
        }]

        print(f"Found country: {country_data['display_name']}")

        oblasts = fetch_children(country_data['lat'], country_data['lon'], country_id, 'administrative')
        result.extend(oblasts)

        return result
    except Exception as e:
        print(f"Error fetching country data: {e}")
        return []

def run():
    data = fetch_regions(COUNTRY)
    with open('locations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Data saved to locations.json')

if __name__ == '__main__':
    run()
