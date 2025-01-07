import requests

from dto.api_input import BaseDTO
from service.implementation.auto_request_api.logic_auto_request import token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict
from datetime import datetime
from database.models import Sport

from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_host, get_sport_name


class AbstractSportDataManager:
    _host: str
    _sport_name: str

    _data_object: BaseDTO

    def __init__(self, new_data: Dict):
        pass

    def main_request(self, host, name, url, blob_name):
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[0]
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        if "teams/teams" in blob_name:
            query = (
                SessionLocal.query(
                    Sport.sport_id,
                    Sport.sport_name
                )
                .filter(Sport.sport_name == blob_name)
            )
            ix = query.first()

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