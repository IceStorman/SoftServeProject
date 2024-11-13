from azure.storage.blob import BlobServiceClient
import json
from typing import Dict
import os
from dotenv import load_dotenv
import datetime
from requests import session
from database.models import BlobIndex, News, Sport, SportIndex
from sqlalchemy.orm import Session
from database.session import SessionLocal
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

def blob_autosave_api(json_data, api: Dict[str, str]) -> None:
    selected_sport = api["name"]
    key = sastokens_dict[selected_sport]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client(api["name"])
    blob_name = f"{api['index'].replace(' ', '_').lower()}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)
    print(f"JSON успішно збережено в Blob Storage як {blob_name}.")
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
    with SessionLocal() as session:
        save_blob_indexes_to_db(selected_sport, blob_name, session)


required_keys = ['header', 'body', 'sport']
def blob_save_news(json_data: Dict[str, Dict[str, str]]) -> None:
    try:
        if not isinstance(json_data, dict):
            raise ValueError("Очікується формат JSON (dict), але отримано інший тип даних.")
        for key in required_keys:
            if key not in json_data:
                raise ValueError(f"JSON-дані мають містити поле '{key}', але воно відсутнє.")
        if 'title' not in json_data['header'] or not json_data['header']['title']:
            raise ValueError(f"JSON-дані мають містити поле '['header']['title']', але воно відсутнє")
    except ValueError as e:
        print(f"Помилка перевірки JSON: {e}")
        return
    name = json_data['header']['title']
    key = sastokens_dict["news"]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client("news")
    blob_name = f"{name.replace(' ', '_').lower()}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)
    with SessionLocal() as session:
        save_news_index_to_db(blob_name, session)


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
        # Перевірка, чи існує спорт у БД
        print(selected_sport)
        sport = session.query(Sport).filter_by(sport_name=selected_sport).first()
        if not sport:
            # Додавання нового виду спорту, якщо його немає в БД
            sport = Sport(sport_name=selected_sport)
            session.add(sport)
            session.commit()

        # Перевірка чи існує запис в таблиці SportsIndex
        sport_index = session.query(SportIndex).filter_by(sport_id=sport.sport_id).first()
        if not sport_index:
            # Додавання нового індексу для виду спорту, якщо його немає в БД
            sport_index = SportIndex(sport_id=sport.sport_id)
            session.add(sport_index)
            session.commit()

        # Перевірка чи існує запис в таблиці BlobIndex
        blob_index = session.query(BlobIndex).filter_by(sports_index_id=sport_index.index_id, filename=blob_name).first()
        if not blob_index:
            # Додавання нового запису для блобу, якщо його немає в БД
            blob_index = BlobIndex(sports_index_id=sport_index.index_id, filename=blob_name)
            session.add(blob_index)
            session.commit()

        print(f"Інформація успішно збережена в БД для блобу: {blob_name}")
    except Exception as e:
        session.rollback()
        print(f"Помилка при збереженні індексів в БД: {e}")

def get_all_blob_indexes_from_db(session, pattern: str):
    blob_indexes = session.query(BlobIndex).filter(BlobIndex.filename.like(f"%{pattern}%")).all()
    return blob_indexes

def get_blob_data_for_all_sports(blob_indexes, session):
    all_results = []
    for blob_index in blob_indexes:
        sport_index = session.query(SportIndex).filter_by(index_id=blob_index.sports_index_id).first()
        if not sport_index:
            print(f"SportIndex для блобу {blob_index.blob_id} не знайдений.")
            continue
        sport = session.query(Sport).filter_by(sport_id=sport_index.sport_id).first()
        if not sport:
            print(f"Sport для SportIndex {sport_index.index_id} не знайдений.")
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
                print(f"Помилка при отриманні блобу '{blob_index.filename}' для виду спорту '{related_sport.sport_name}': {e}")
                
    return json.dumps(all_results, ensure_ascii=False) if all_results else json.dumps({"error": "No data found"})

def save_news_index_to_db(blob_name: str, session) -> None:
    try:
        # Перевірка, чи існує новина з таким blob_name
        existing_news = session.query(News).filter_by(blob_name=blob_name).first()
        if existing_news:
            print(f"Новина '{blob_name}' вже існує в БД.")
            return
        news_index = News(blob_id=blob_name, save_at=datetime.utcnow())
        session.add(news_index)
        print(f"Новина '{blob_name}' збережена в БД.")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Помилка при збереженні індексу новини в БД: {e}")

def get_news_by_index(blob_name: str, session) -> Dict:
    news_record = session.query(News).filter_by(blob_name=blob_name).first()
    if not news_record:
        print(f"Новина з blob_name '{blob_name}' не знайдена в БД.")
        return {}
    try:
        data = blob_get_news(news_record)
        return data
    except Exception as e:
        print(f"Помилка при отриманні блобу '{news_record}': {e}")


def get_news_by_count(count: int, session) -> str:
    news_records = session.query(News).order_by(News.save_at.desc()).limit(count).all()
    if not news_records:
        print(f"Новини в БД не знайдені.")
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
            print(f"Помилка при отриманні блобу '{news_record.blob_id}': {e}")
    return json.dumps(all_results, ensure_ascii=False)

'''
with SessionLocal() as session:
    # Отримуємо всі індекси блобів
    a = get_all_blob_indexes_from_db(session, "players/players?team=333&season=2024.json")
    print("Отримані індекси блобів:", a)

    # Використовуємо отримані індекси для отримання даних
    b = get_blob_data_for_all_sports(a, session)
    print("Дані блобів:", b)
'''

