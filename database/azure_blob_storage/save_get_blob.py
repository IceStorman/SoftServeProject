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

SUSPICIOUS_DOMAINS = ["malicious.com", "phishing.net", "unsafe.io"]
# Рівні загрози
THREAT_LEVELS = {
    "low": "\033[33m[LOW]\033[0m",
    "medium": "\033[33m[MEDIUM]\033[0m",
    "high": "\033[31m[HIGH]\033[0m"
}
SUSPICIOUS_PATTERNS = [
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


def validate_json_structure(json_data):
    if not isinstance(json_data, dict):
        raise ValueError("\033[31mExpected JSON (dict) format, but received a different data type.\033[0m")
    if 'title' not in json_data:
        raise ValueError(f"\033[31mJSON data should contain the field '['header']['title']', but it is missing or empty.\033[0m")


def check_json(json_data):
    try:
        validate_json_structure(json_data)
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
    if check_json(json_data):
        print("\033[32mAll good in file.\033[0m")
        name = json_data['title']
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


def fetch_blob_data(news_records) -> list:
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
    return all_results


def handle_no_records_message(message: str) -> str:
    print(f"\033[31m{message}\033[0m")
    return json.dumps([])


def get_news_by_teams(count: int, team_names: list[str], session) -> str:
    team_news_ids = (
        session.query(TeamIndex.news_id)
        .filter(TeamIndex.team_name.in_(team_names))
        .distinct()
        .all()
    )
    team_news_ids = [id[0] for id in team_news_ids]

    if not team_news_ids:
        return handle_no_records_message(f"No news found for the specified teams: {team_names}")

    news_records = (
        session.query(News)
        .filter(News.news_id.in_(team_news_ids))
        .order_by(News.save_at.desc())
        .limit(count)
        .all()
    )

    if not news_records:
        return handle_no_records_message(f"No news found for the specified teams: {team_names}")

    return json.dumps(fetch_blob_data(news_records), ensure_ascii=False)


def get_news_by_sport(count: int, sport_name: str, session) -> str:
    sport = session.query(Sport).filter_by(sport_name=sport_name).first()
    if not sport:
        return handle_no_records_message(f"Sport '{sport_name}' was not found in the database.")

    news_records = (
        session.query(News)
        .filter_by(sport_id=sport.sport_id)
        .order_by(News.save_at.desc())
        .limit(count)
        .all()
    )

    if not news_records:
        return handle_no_records_message(f"No news found for sport '{sport_name}'.")

    return json.dumps(fetch_blob_data(news_records), ensure_ascii=False)


def get_news_by_count(count: int, session) -> str:
    news_records = session.query(News).order_by(News.save_at.desc()).limit(count).all()
    if not news_records:
        return handle_no_records_message("No news was found in the database.")
    return json.dumps(fetch_blob_data(news_records), ensure_ascii=False)


with SessionLocal() as session:
    print(get_news_by_count(2, session))
    print(get_news_by_sport(3, "football", session))
    print(get_news_by_teams(3, ["g"], session))

a = {
    'timestamp': '2024-11-20',
    'article': {
        'section_1': {
            'title': 'Introduction',
            'content': ['This is the introduction paragraph.'],
            'images': ['https://www.google.com/imgres?q=png%20sport%20nba&imgurl=https%3A%2F%2Fwww.pngarts.com%2Ffiles%2F12%2FNBA-Player-PNG-Image.png&imgrefurl=https%3A%2F%2Fwww.pngarts.com%2Fexplore%2F263429&docid=6qV5t19iJnnrCM&tbnid=gVskAEIkQhikZM&vet=12ahUKEwj6m6SBueuJAxUVgv0HHe8TGAYQM3oECGYQAA..i&w=528&h=392&hcb=2&ved=2ahUKEwj6m6SBueuJAxUVgv0HHe8TGAYQM3oECGYQAA', 'https://www.google.com/imgres?q=png%20sport%20nba&imgurl=https%3A%2F%2Fe7.pngegg.com%2Fpngimages%2F509%2F262%2Fpng-clipart-basketball-moves-oklahoma-city-thunder-basketball-player-nba-nba-sport-jersey.png&imgrefurl=https%3A%2F%2Fwww.pngegg.com%2Fen%2Fpng-bghgy&docid=BBHR4SqFahOUZM&tbnid=Ni-5-sVaJOxvYM&vet=12ahUKEwj6m6SBueuJAxUVgv0HHe8TGAYQM3oECE4QAA..i&w=900&h=512&hcb=2&ved=2ahUKEwj6m6SBueuJAxUVgv0HHe8TGAYQM3oECE4QAA'],            'subheadings': ['Subheading 1']
        },
        'section_2': {
            'title': 'Details',
            'content': ['Details about the article.'],
            'images': ['image_url_3.jpg'],
            'subheadings': []
        }
    }
}

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
'''
test_json = {

    "title": "nba maybe work",
    "body": "bnhjijughhy",
    "file": {
        "name": "malicious",
    },
    "sport": "nba",
    "img": "data:image/jpeg;base64,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"
}
test_json1 = {

    "title": "nba match",
    "body": "bnhjijughhy",
    "file": {
        "name": "malicious",
    },
    "sport": "nba",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKnWDXTdQP2z1f9xcf5VLdAaifmIWCWQO6JQ&s"
}
blob_save_news(test_json)
blob_save_news(test_json1)