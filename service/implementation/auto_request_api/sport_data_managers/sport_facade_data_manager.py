import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

from service.implementation.auto_request_api.sport_data_managers.afl_data_manager import AflDataManager
from service.implementation.auto_request_api.sport_data_managers.baseball_data_manager import BaseballDataManager
from service.implementation.auto_request_api.sport_data_managers.football_data_manager import FootballDataManager
from service.implementation.auto_request_api.sport_data_managers.formula_one_data_manager import FormulaOneDataManager
from service.implementation.auto_request_api.sport_data_managers.handball_data_manager import HandballDataManager
from service.implementation.auto_request_api.sport_data_managers.hockey_data_manager import HockeyDataManager
from service.implementation.auto_request_api.sport_data_managers.mma_data_manager import MmaDataManager
from service.implementation.auto_request_api.sport_data_managers.nba_data_manager import NbaDataManager
from service.implementation.auto_request_api.sport_data_managers.nfl_data_manager import NflDataManager
from service.implementation.auto_request_api.sport_data_managers.rugby_data_manager import RugbyDataManager
from service.implementation.auto_request_api.sport_data_managers.volleyball_data_manager import VolleyballDataManager


class SportFacadeDataManager:
    data_managers: Dict[str, AbstractSportDataManager] = {
            "football": FootballDataManager(),
            "afl": AflDataManager(),
            "baseball": BaseballDataManager(),
            "basketball": BaseballDataManager(),
            "formula_one": FormulaOneDataManager(),
            "handball": HandballDataManager(),
            "hockey": HockeyDataManager(),
            "mma": MmaDataManager(),
            "nba": NbaDataManager(),
            "nfl": NflDataManager(),
            "rugby": RugbyDataManager(),
            "volleyball": VolleyballDataManager()
        }

    @staticmethod
    def get_data_manager(self, sport_name: str) -> AbstractSportDataManager:
        return self.data_managers[sport_name]

