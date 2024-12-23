import requests

from dto.api_input import BaseDTO
from service.implementation.auto_request_api.logic_auto_request import current_key_index, token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class AbstractSportDataManager:
    api_data: Dict[str, str]

    _sport_name: str
    _host: str

    _data_object: BaseDTO

    def __init__(self, new_data_object: BaseDTO, new_sport_name: str):
        self._sport_name = new_sport_name

    def main_request(self, host, url, blob_name) -> Dict[str, str]:
        global current_key_index, account_url

        if token_usage[self._sport_name] >= 99:
            current_key_index = (current_key_index + 1) % len(api_key)
            token_usage[self._sport_name] = 0

        token_usage[self._sport_name] += 1
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[current_key_index]
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        blob_save_specific_api(self._sport_name, blob_name, json_data)

        return json_data

    def try_return_json_data(self, url: str, index: str) -> Dict[str, str]:
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                return result
        try:
            json_data = self.main_request(self._host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}