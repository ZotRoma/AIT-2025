import requests
import json
import time

def get_public_matches(min_match_id=None):
    url = "https://api.opendota.com/api/proMatches"
    if min_match_id:
        url += f"?less_than_match_id={min_match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Не удалось загрузить данные")
        return None

all_matches = []
min_match_id = None
for _ in range(10):  # Загружаем 10 страниц по 100 матчей
    matches = get_public_matches(min_match_id)
    if matches:
        all_matches.extend(matches)
        min_match_id = min([match['match_id'] for match in matches])
        time.sleep(1)  # Пауза для соблюдения лимитов
    else:
        break

with open('pro_matches.json', 'w') as f:
    json.dump(all_matches, f, indent=4)