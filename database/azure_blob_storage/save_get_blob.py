from azure.storage.blob import BlobServiceClient
import json
from typing import Dict
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from database.models import BlobIndex, News, Sport, SportIndex, TeamIndex
from database.session import SessionLocal
import re


load_dotenv()
account_url = os.getenv("BLOBURL")
sastokens_dict = {
    "football": os.getenv("SASFOOTBALL"),
    "basketball": os.getenv("SASBASKETBALL"),
    "volleyball": os.getenv("SASVOLLEYBALL"),
    "afl": os.getenv("SASAFL"),
    "baseball": os.getenv("SASBASEBALL"),
    "formula-1": os.getenv("SASFORMULA1"),
    "handball": os.getenv("SASHANDBALL"),
    "hockey": os.getenv("SASHOCKEY"),
    "mma": os.getenv("SASMMA"),
    "nba":  os.getenv("SASNBA"),
    "nfl": os.getenv("SASNFL"),
    "rugby": os.getenv("SASRUGBY"),
    "news": os.getenv("SASNEWS"),
}

required_keys = ['header', 'body', 'sport']
SUSPICIOUS_DOMAINS = ["malicious.com", "phishing.net", "unsafe.io"]
# Рівні загрози
THREAT_LEVELS = {
    "low": "\033[33m[LOW]\033[0m",
    "medium": "\033[33m[MEDIUM]\033[0m",
    "high": "\033[31m[HIGH]\033[0m"
}
SUSPICIOUS_PATTERNS = [
    r"(?:http|https)://[^\s]+",  # Посилання
    r"<script.*?>.*?</script>",  # Вбудовані скрипти
    r"data:[^;]+;base64,",  # Base64-кодовані файли
    r"\.exe|\.bat|\.sh|\.py"  # Небезпечні розширення
]


def blob_autosave_api(json_data, api: Dict[str, str]) -> None:
    selected_sport = api["name"]
    key = sastokens_dict[selected_sport]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client(api["name"])
    blob_name = f"{api['index'].replace(' ', '_').lower()}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)
    print(f"\033[32mJSON auto saved to Blob Storage as {blob_name}.\033[0m")
    with SessionLocal() as session:
        save_blob_indexes_to_db(selected_sport, blob_name, session)


def blob_save_specific_api(name: str, blob_name: str, json_data: Dict[str, str]) -> None:
    selected_sport = name
    key = sastokens_dict[selected_sport]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client(name)
    blob_name = f"{blob_name}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)
    print(f"\033[32mJSON specific saved to Blob Storage as {blob_name}.\033[0m")
    with SessionLocal() as session:
        save_blob_indexes_to_db(selected_sport, blob_name, session)


def contains_suspicious_links(data, parent_key=""):
    found_suspicious = []
    if isinstance(data, dict):
        for key, value in data.items():
            found_suspicious.extend(
                contains_suspicious_links(value, f"{parent_key}.{key}" if parent_key else key)
            )
    elif isinstance(data, list):
        for index, item in enumerate(data):
            found_suspicious.extend(
                contains_suspicious_links(item, f"{parent_key}[{index}]")
            )
    elif isinstance(data, str):
        # Перевірка за доменами
        for domain in SUSPICIOUS_DOMAINS:
            if domain in data:
                found_suspicious.append((parent_key, data, "medium"))
        # Перевірка за патернами
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, data):
                # Визначення рівня загрози
                threat_level = "high"
                found_suspicious.append((parent_key, data, threat_level))

    return found_suspicious


def validate_json_structure(json_data, required_keys):
    if not isinstance(json_data, dict):
        raise ValueError("\033[31mExpected JSON (dict) format, but received a different data type.\033[0m")
    for key in required_keys:
        if key not in json_data:
            raise ValueError(f"\033[31mJSON data should contain the field '{key}', but it is missing.\033[0m")
    if 'title' not in json_data['header'] or not json_data['header']['title']:
        raise ValueError(f"\033[31mJSON data should contain the field '['header']['title']', but it is missing or empty.\033[0m")


def check_json(json_data, required_keys):
    try:
        validate_json_structure(json_data, required_keys)
        results = contains_suspicious_links(json_data)
        if results:
            print("\033[31mPotential threats detected:\033[0m")
            for path, content, level in results:
                print(f"{THREAT_LEVELS[level]} Field: {path} | Content: {content}")
                raise ValueError("\033[31mJSON contains suspicious content and cannot be saved.\033[0m")
        else:
            print("\033[32mNo threats detected in JSON.\033[0m")
    except ValueError as e:
        print(f"\031[31mJSON validation error: {e}\033[0m")
        return False
    print("\033[32mJSON passed all validation checks.\033[0m")
    return True


def blob_save_news(json_data: Dict[str, Dict[str, str]]) -> None:
    if check_json(json_data, required_keys):
        print("\033[32mAll good in file.\033[0m")
        name = json_data['header']['title']
        key = sastokens_dict["news"]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client("news")
        blob_name = f"{name.replace(' ', '_').lower()}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(json_data), overwrite=True)
        with SessionLocal() as session:
            save_news_index_to_db(blob_name, json_data, session)
    else:
        print("\033[31mThe file does not meet the requirements.\033[0m")


def blob_get_data(blob_index: str, sport_index: str) -> dict:
    try:
        key = sastokens_dict[sport_index]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client(sport_index)
        blob_client = container_client.get_blob_client(blob_index)
        blob_data = blob_client.download_blob()
        json_data = json.loads(blob_data.readall())
        return json_data
    except Exception as e:
        return {"error": str(e)}


def blob_get_news(news_index: str) -> dict:
    try:
        key = sastokens_dict["news"]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client("news")
        blob_client = container_client.get_blob_client(news_index)
        blob_data = blob_client.download_blob()
        json_data = json.loads(blob_data.readall())
        return json_data
    except Exception as e:
        return {"error": str(e)}


def save_blob_indexes_to_db(selected_sport: str, blob_name: str, session) -> None:
    try:
        sport = session.query(Sport).filter_by(sport_name=selected_sport).first()
        if not sport:
            sport = Sport(sport_name=selected_sport)
            session.add(sport)
            session.commit()

        sport_index = session.query(SportIndex).filter_by(sport_id=sport.sport_id).first()
        if not sport_index:
            sport_index = SportIndex(sport_id=sport.sport_id)
            session.add(sport_index)
            session.commit()

        blob_index = session.query(BlobIndex).filter_by(sports_index_id=sport_index.index_id, filename=blob_name).first()
        if not blob_index:
            blob_index = BlobIndex(sports_index_id=sport_index.index_id, filename=blob_name)
            session.add(blob_index)
            session.commit()

        print(f"\033[32mThe information is successfully saved in the DB for the blob:\033[0m {blob_name}")
    except Exception as e:
        session.rollback()
        print(f"\033[31mError when saving indexes in the database: {e}\033[0m")


def get_all_blob_indexes_from_db(session, pattern: str):
    blob_indexes = session.query(BlobIndex).filter(BlobIndex.filename.like(f"%{pattern}%")).all()
    return blob_indexes


def get_blob_data_for_all_sports(session, blob_indexes):
    all_results = []
    for blob_index in blob_indexes:
        sport_index = session.query(SportIndex).filter_by(index_id=blob_index.sports_index_id).first()
        if not sport_index:
            print(f"\033[31mSportIndex for blob: {blob_index.blob_id} not found.\033[0m")
            continue
        sport = session.query(Sport).filter_by(sport_id=sport_index.sport_id).first()
        if not sport:
            print(f"\033[31mSport for SportIndex {sport_index.index_id} not found.\033[0m")
            continue
        related_sports = session.query(Sport).filter_by(sport_name=sport.sport_name).all()
        for related_sport in related_sports:
            try:
                data = blob_get_data(blob_index.filename, related_sport.sport_name.lower())
                all_results.append({
                    "sport": related_sport.sport_name,
                    "blob_name": blob_index.filename,
                    "data": data
                })
            except Exception as e:
                print(f"\033[31mError retrieving blob '{blob_index.filename}' for sport '{related_sport.sport_name}': {e}\033[0m")
    return json.dumps(all_results, ensure_ascii=False) if all_results else json.dumps({"error": "No data found"})


def save_news_index_to_db(blob_name: str, json_data,  session) -> None:
    try:
        existing_news = session.query(News).filter_by(blob_id=blob_name).first()
        if existing_news:
            print(f"\033[31mNews '{blob_name}' already exists in the database.\033[0m")
            return
        sport = session.query(Sport).filter_by(sport_name=json_data["sport"]).first()
        if not sport:
            return
        news_index = News(
            blob_id=blob_name,
            save_at=datetime.now(timezone.utc),
            sport_id=sport.sport_id,
        )
        session.add(news_index)
        print(f"\033[32mThe news item '{blob_name}' is saved in the database.\033[0m")
        session.commit()

        for team_name in json_data["team_names"]:
            team_index = TeamIndex(
                news_id=news_index.news_id,
                team_name=team_name
            )
            session.add(team_index)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"\033[31mError when saving the news index in the database: {e}\033[0m")


def get_news_by_index(blob_name: str, session) -> Dict:
    news_record = session.query(News).filter_by(blob_id=blob_name).first()
    if not news_record:
        print(f"\033[31mNews with blob_name '{blob_name}' not found in database.\033[0m")
        return {}
    try:
        data = blob_get_news(news_record)
        return data
    except Exception as e:
        print(f"\033[31mError retrieving blob '{news_record}': {e}\033[0m")


def get_news_by_count(count: int, session) -> str:
    news_records = session.query(News).order_by(News.save_at.desc()).limit(count).all()
    if not news_records:
        print(f"\033[31mNo news was found in the database.\033[0m")
        return json.dumps([])
    all_results = []
    for news_record in news_records:
        try:
            data = blob_get_news(news_record.blob_id)
            all_results.append({
                "blob_id": news_record.blob_id,
                "data": data
            })
        except Exception as e:
            print(f"\033[31mError while receiving blob '{news_record.blob_id}': {e}\033[0m")
    return json.dumps(all_results, ensure_ascii=False)

'''

with SessionLocal() as session:
    result = get_news_by_count(2, session)
    print(result)
with SessionLocal() as session:
    # Отримуємо всі індекси блобів
    a = get_all_blob_indexes_from_db(session, "players/players?team=333&season=2024.json")
    print("Отримані індекси блобів:", a)

    # Використовуємо отримані індекси для отримання даних
    b = get_blob_data_for_all_sports(a, session)
    print("Дані блобів:", b)
    
test_json = {
    "header": {
        "title": "Safe JSON",
        "links": ["http://malicious-site.com/virus.exe", "http://safe-site.com"]
    },
    "body": "<script>alert('Hacked!');</script>",
    "file": {
        "name": "malicious.exe",
        "data": "data:application/octet-stream;base64,VGhpcyBpcyBhIHRlc3Q="
    },
    "sport": "football"

}
blob_save_news(test_json)
'''
