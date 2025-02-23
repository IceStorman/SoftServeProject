import requests
from dto.api_input import BaseDTO
from service.implementation.auto_request_api.logic_auto_request import api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, \
    get_blob_data_for_all_sports, get_specific_blob_filename_from_db
from database.session import SessionLocal
from typing import Dict
from database.postgres.save_data import save_api_data


class AbstractSportDataManager:
    _host: str
    _sport_name: str
    _sport_id: int

    _data_object: BaseDTO
    _data_dict: Dict

    def __init__(self, new_data):
        self._data_dict = new_data

    def __main_request(self, host, name, url, blob_name):
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[0]
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if "teams/teams" in blob_name:
            save_api_data(json_data, name)
            return json_data
        blob_save_specific_api(name, blob_name, json_data)
        save_api_data(json_data, self._sport_name)
        return json_data
    

    def _return_specific_json_data(self, url: str, index: str, sport_id: int) -> Dict[str, str]:
        with SessionLocal() as session:
            check = get_specific_blob_filename_from_db(session, index, sport_id)
            if check:
                result = get_blob_data_for_all_sports(session, [check])
                return result
        try:
            json_data = self.__main_request(self._host, self._sport_name, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}