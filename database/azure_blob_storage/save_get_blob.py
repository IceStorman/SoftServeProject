from azure.storage.blob import BlobServiceClient
import json
from typing import Dict
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from database.models import BlobIndex, News, Sport, SportIndex, TeamIndex, TeamInNews
from database.session import SessionLocal
from exept.colors_text import print_error_message, print_good_message
import re

from service.implementation.email_sender.email_sender import try_send_email_to_users

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
    "nfl": os.getenv("SASNFL"),
    "rugby": os.getenv("SASRUGBY"),
    "news": os.getenv("SASNEWS"),
}

img = {
    "football": "https://images.vexels.com/media/users/3/234566/isolated/preview/a66aee6975507c1c26fd158989ab53f9-man-soccer-kicking-football-flat.png?w=360",
    "mma": "https://www.api-football.com/public/img/home1/mma-logo.png",
    "hockey": "https://www.api-football.com/public/img/home1/hockey-logo.png",
    "afl": "https://www.api-football.com/public/img/home1/afl-logo.png",
    "baseball": "https://www.api-football.com/public/img/home1/baseball-logo.png",
    "basketball": "https://cdni.iconscout.com/illustration/premium/thumb/man-who-is-dribbling-a-basketball-illustration-download-in-svg-png-gif-file-formats--dribble-skills-drills-sports-activities-pack-games-illustrations-8022188.png?f=webp",
    "formula-1": "https://www.api-football.com/public/img/news/f1-mini.png",
    "nfl": "https://www.api-football.com/public/img/home1/nfl-logo.png",
    "rugby": "https://www.api-football.com/public/img/home1/rugby-logo.png",
    "volleyball": "https://www.api-football.com/public/img/home1/volleyball-logo.png",
    "handball": "https://www.api-football.com/public/img/home1/handball-logo.png"
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
    #r"data:[^;]+;base64,",  # Base64-кодовані файли
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
    print_good_message("JSON auto saved to Blob Storage as {blob_name}.")
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
    print_good_message("JSON specific saved to Blob Storage as {blob_name}.")
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
        raise ValueError (print_error_message("Expected JSON (dict) format, but received a different data type."))
    if 'title' not in json_data:
        raise ValueError(print_error_message("JSON data should contain the field '['header']['title']', but it is missing or empty."))


def check_json(json_data):
    try:
        validate_json_structure(json_data)
        results = contains_suspicious_links(json_data)
        if results:
            print_error_message("Potential threats detected:")
            for path, content, level in results:
                print(f"{THREAT_LEVELS[level]} Field: {path} | Content: {content}")
                raise ValueError(print_error_message("JSON contains suspicious content and cannot be saved."))
        else:
            print_good_message("No threats detected in JSON.")
    except ValueError as e:
        print_error_message("JSON validation error: {e}")
        return False
    print_good_message("JSON passed all validation checks.")
    return True


def sanitize_name(name):
    name = re.sub(r'[^a-zA-Z0-9а-яА-Я]', '-', name)
    name = re.sub(r'_{2,}', '_', name)
    return name.lower()

def blob_save_news(json_data: Dict[str, Dict[str, str]]) -> None:
    if check_json(json_data):
        print_good_message("All good in file.")
        name = json_data['title']
        key = sastokens_dict["news"]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client("news")
        blob_name = f"{sanitize_name(name)}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(json_data), overwrite=True)
        with SessionLocal() as session:
            save_news_index_to_db(blob_name, json_data, session)
    else:
        print_error_message("The file does not meet the requirements.")

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
    
def blob_get_specific_article(session, index_id: int) -> dict:
    try:
    
        blob_index = get_specific_blob_index_from_db(session, index_id)
        if not blob_index:
            raise ValueError(f"Blob with index ID {index_id} not found in the database.")

       
        sport_index = session.query(SportIndex).filter_by(index_id=blob_index.sports_index_id).first()
        if not sport_index:
            raise ValueError(f"SportIndex for blob index ID {index_id} not found.")

       
        sport = session.query(Sport).filter_by(sport_id=sport_index.sport_id).first()
        if not sport:
            raise ValueError(f"Sport for sport index ID {sport_index.index_id} not found.")

       
        data = blob_get_data(blob_index.filename, sport.sport_name.lower())
        if "error" in data:
            raise ValueError(f"Error retrieving blob data: {data['error']}")

        return data
    except Exception as e:
        print_error_message(f"Error retrieving specific article: {e}")
        return {"error": str(e)}


def save_blob_indexes_to_db(selected_sport: str, blob_name: str, session) -> None:
    try:
        sport = session.query(Sport).filter_by(sport_name=selected_sport).first()
        if not sport:
            sport_img = img[selected_sport]
            sport = Sport(sport_name=selected_sport, sport_img=sport_img)
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

        print_good_message(f"The information is successfully saved in the DB for the blob: {blob_name}")
    except Exception as e:
        session.rollback()
        print_error_message(f"Error when saving indexes in the database: {e}")

def get_all_blob_indexes_from_db(session, pattern: str):
    blob_indexes = session.query(BlobIndex).filter(BlobIndex.filename.like(f"%{pattern}%")).all()
    return blob_indexes

def get_specific_blob_index_from_db(session, index_id:int):
    index = session.query(BlobIndex).filter(BlobIndex.blob_id == index_id).first()
    return index

def get_blob_data_for_all_sports(session, blob_indexes):
    all_results = []
    for blob_index in blob_indexes:
        sport_index = session.query(SportIndex).filter_by(index_id=blob_index.sports_index_id).first()
        if not sport_index:
            print_error_message(f"SportIndex for blob: {blob_index.blob_id} not found.")
            continue
        sport = session.query(Sport).filter_by(sport_id=sport_index.sport_id).first()
        if not sport:
            print_error_message(f"Sport for SportIndex {sport_index.index_id} not found.")
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
                print_error_message(f"Error retrieving blob '{blob_index.filename}' for sport '{related_sport.sport_name}': {e}")
    return json.dumps(all_results, ensure_ascii=False) if all_results else json.dumps({"error": "No data found"})


def save_news_index_to_db(blob_name: str, json_data,  session) -> None:
    try:
        existing_news = session.query(News).filter_by(blob_id=blob_name).first()
        if existing_news:
            print_error_message(f"News '{blob_name}' already exists in the database.")
            return
        print(json_data["team_names"])
        sport = session.query(Sport).filter_by(sport_name=json_data["S_P_O_R_T"]).first()
        if not sport:
            return
        news_index = News(
            blob_id=blob_name,
            save_at=datetime.now(timezone.utc),
            sport_id=sport.sport_id,
        )
        session.add(news_index)
        print_good_message(f"The news item '{blob_name}' is saved in the database.")
        session.commit()
        teams = session.query(TeamIndex).all()
        team_dict = {team.name: team.team_index_id for team in teams}
        teams = json_data["team_names"]
        print(teams)
        for team_name in teams:
            if isinstance(team_name, list):
                for name in team_name:
                    team_index_id = team_dict.get(name, None)
                    if team_index_id is not None:
                        team_index = TeamInNews(
                            news_id=news_index.news_id,
                            name=name,
                            team_index_id=team_index_id
                        )
                        session.add(team_index)
            else:
                team_index_id = team_dict.get(team_name, None)
                if team_index_id is not None:
                    team_index = TeamInNews(
                        news_id=news_index.news_id,
                        name=team_name,
                        team_index_id=team_index_id
                    )
                    session.add(team_index)

        session.commit()
    except Exception as e:
        session.rollback()
        print_error_message(f"Error when saving the news index in the database: {e}")


def get_news_by_index(blob_name: str, session) -> Dict:
    news_record = session.query(News).filter_by(blob_id=blob_name).first()
    if not news_record:
        print_error_message(f"News with blob_name '{blob_name}' not found in database")
        return {}
    try:
        data = blob_get_news(news_record)
        return data
    except Exception as e:
        print_error_message(f"Error retrieving blob '{news_record}': {e}")


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
            print_error_message(f"Error while receiving blob '{news_record.blob_id}': {e}")
    return all_results


def handle_no_records_message(message: str) -> str:
    print_error_message(f"{message}")
    return json.dumps([])


def get_news_by_teams(count: int, team_names: list[str], session) -> str:
    team_news_ids = (
        session.query(TeamIndex.news_id)
        .filter(TeamIndex.name.in_(team_names))
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
