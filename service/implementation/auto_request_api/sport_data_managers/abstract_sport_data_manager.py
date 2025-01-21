import requests

from dto.api_input import BaseDTO
from service.implementation.auto_request_api.logic_auto_request import token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict
from datetime import datetime
from database.models.sports import Sport
from database.postgres.save_data import save_api_data
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_host


class AbstractSportDataManager:
    _host: str
    _sport_name: str

    _data_object: BaseDTO
    _data_dict: Dict

    def __init__(self, new_data: Dict):
        self._data_dict = new_data

        query = (
            SessionLocal().query(
                Sport.sport_id,
                Sport.sport_name
            )
            .filter(Sport.sport_id == new_data.get("sport_id"))
        )
        print(query)
        ix = query.first()
        if ix is not None:
            self._sport_name = ix.sport_name

    def main_request(self, host, name, url, blob_name):
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[0]
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        print(json_data)
        print(name)
        if "teams/teams" in blob_name:
            save_api_data(json_data, name)
            return json_data
        blob_save_specific_api(name, blob_name, json_data)
        return json_data

    def try_return_json_data(self, url: str, index: str) -> Dict[str, str]:
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                return result
        try:
            json_data = self.main_request(self._host, self._sport_name, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}