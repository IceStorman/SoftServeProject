from typing import Optional

from dependency_injector.wiring import Provide

from api.container.container import Container
from database.models import Sport
from database.session import SessionLocal
from dto.common_response import CommonResponse
from service.api_logic.player_logic import PlayerService
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_players_index, get_players_url, get_host


class PlayersDataManager(AbstractSportDataManager):
    _team_id: Optional[int]
    _league_id: Optional[int]
    _search: Optional[str]

    _service: PlayerService = Provide[Container.players_service]


    def __init__(self, new_data):
        super().__init__(new_data)

        query = (
            SessionLocal().query(
                Sport.sport_id,
                Sport.sport_name
            )
            .filter(Sport.sport_id == new_data.sport_id)
        )

        ix = query.first()

        if ix is not None:
            self._sport_name = ix.sport_name
            self._host = get_host(self._sport_name)

        self._team_id = new_data.team_id
        self._league_id = new_data.league_id
        self._search = new_data.name
        self._sport_id = new_data.sport_id
        self.__filters_data = new_data.filters_data


    def get_data(self):
        index = get_players_index(self._sport_name, self._team_id, self._league_id, self._search)
        result = self._service.get_teams_filtered(self.__filters_data)
        if result["count"]:
            return result

        url = get_players_url(self._sport_name, self._team_id, self._league_id, self._search)

        try:
            team = self._return_specific_json_data(url, index, self._sport_id)
            return team
        except Exception as e:
            return {"error": str(e)}