import requests

from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

from service.implementation.auto_request_api.sport_data_managers.afl_data_manager import AflDataManager
from service.implementation.auto_request_api.sport_data_managers.baseball_data_manager import BaseballDataManager
from service.implementation.auto_request_api.sport_data_managers.basketball_data_manager import BasketballDataManager
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
    @staticmethod
    def get_data_manager(sport_name: str, api_data: Dict[str, str]) -> AbstractSportDataManager:
        match sport_name:
            case "football":
                return FootballDataManager(api_data)
            case "baseball":
                return BaseballDataManager(api_data)
            case "basketball":
                return BasketballDataManager(api_data)
            case "handball":
                return HandballDataManager(api_data)
            case "hockey":
                return HockeyDataManager(api_data)
            case "afl":
                return AflDataManager(api_data)
            case "formula_one":
                return FormulaOneDataManager(api_data)
            case "mma":
                return MmaDataManager(api_data)
            case "nba":
                return NbaDataManager(api_data)
            case "nfl":
                return NflDataManager(api_data)
            case "rugby":
                return RugbyDataManager(api_data)
            case "volleyball":
                return VolleyballDataManager(api_data)
            case _:
                return AbstractSportDataManager(api_data)



