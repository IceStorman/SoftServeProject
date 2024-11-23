from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from datetime import datetime
import json


def get_games_today(session):
    blob_indexes = get_all_blob_indexes_from_db(session, "games.json") + \
                   get_all_blob_indexes_from_db(session, "fixtures.json")
    result = get_blob_data_for_all_sports(session, blob_indexes)
    today = datetime.now().date()
    data = json.loads(result)
    filtered_data = []

    for sport_data in data:
        if 'data' in sport_data and 'response' in sport_data['data']:
            matches = sport_data['data']['response']
            # Фільтруємо лише ті матчі, що мають дату сьогодні
            today_matches = []
            for match in matches:
                match_date = match.get('date')
                if match_date and isinstance(match_date, str):
                    try:
                        if datetime.fromisoformat(match_date).date() == today:
                            today_matches.append(match)
                    except ValueError:
                        continue

            if today_matches:
                filtered_data.append({
                    "sport": sport_data.get("sport"),
                    "blob_name": sport_data.get("blob_name"),
                    "matches": today_matches
                })

    return filtered_data
