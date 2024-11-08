from azure.storage.blob import BlobServiceClient
import json
from typing import Dict
import os
from dotenv import load_dotenv
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

    #save_blob_indexes_to_db(api, blob_name, session)


def blob_save_specific_api(name: str, blob_name: str, json_data: Dict[str, str]) -> None:
    selected_sport = name
    key = sastokens_dict[selected_sport]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client(name)
    blob_name = f"{blob_name}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)

    #save_blob_indexes_to_db(api, blob_name, session)


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

'''
def save_blob_indexes_to_db(api: Dict[str, str], blob_name: str, session) -> None:
    try:
        # Перевірка, чи існує спорт у БД
        sport = session.query(Sport).filter_by(name=api['name']).first()
        if not sport:
            # Якщо спорту немає, створюємо новий
            sport = Sport(name=api['name'])
            session.add(sport)
            session.commit()
        # Збереження індексу виду спорту
        sport_index = SportIndex(sport_id=sport.id, sport_index=api['index'])
        session.add(sport_index)
        session.commit()
        # Збереження індексу блобу
        blob_index = BlobIndex(sport_index_id=sport_index.id, blob_name=blob_name)
        session.add(blob_index)
        session.commit()

        print(f"Інформація успішно збережена в БД для блобу: {blob_name}")
    except Exception as e:
        session.rollback()
        print(f"Помилка при збереженні індексів в БД: {e}")

def get_all_blob_indexes_from_db(session, pattern: str):
    # Шукаємо всі записи в таблиці BlobIndex, що містять "games" в імені блоба
    blob_indexes = session.query(BlobIndex).filter(BlobIndex.blob_name.like(f"%{pattern}%")).all()
    return blob_indexes

def get_blob_data_for_all_sports(blob_indexes, session):
    all_results = []
    for blob_index in blob_indexes:
        # Отримуємо відповідний SportIndex
        sport_index = session.query(SportIndex).filter_by(id=blob_index.sport_index_id).first()
        if sport_index:
            # Отримуємо спортивний ID (наприклад, для футболу)
            sport = session.query(Sport).filter_by(id=sport_index.sport_id).first()
            if sport:
                # Підключаємося до Blob Storage для відповідного контейнера
                sport_index = sport.name.lower()  # Наприклад, "football"
                blob_index = blob_index.blob_name

                # Отримуємо дані з Blob Storage
                try:
                    data = blob_get_data(blob_index, sport_index)
                    all_results.append({
                        "sport": sport.name,
                        "blob_name": blob_index,
                        "data": data
                    })
                except Exception as e:
                    print(f"Помилка при отриманні блобу '{blob_index}': {e}")
    return all_results
'''
