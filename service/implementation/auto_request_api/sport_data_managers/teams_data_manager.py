from typing import Optional, Dict
from dependency_injector.wiring import Provide
from api.container.container import Container
from database.models import Sport
from database.session import SessionLocal
from service.api_logic.teams_logic import TeamsService
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_host, get_team_index


class TeamsDataManager(AbstractSportDataManager):
    _sport_id: Optional[int]
    _leagues_id: Optional[int]
    _countries_id: Optional[int]
    _page: Optional[int]
    _per_page: Optional[int]

    _service: TeamsService = Provide[Container.teams_service]

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

        self._leagues_id = new_data.league_id
        self._host = get_host(self._sport_name)

        self._page = new_data.page
        self._per_page = new_data.per_page

    def get_teams_data(self, pagination):
        index = get_team_index(self._sport_name, self._leagues_id)
        result = self._service.get_teams_filtered(self._data_dict, pagination)
        if result:
            return result
        url_first = get_host(self._sport_name)
        url = "https://"+url_first+"/"+index.replace("teams/","")
        try:
            team = self._try_return_json_data(url, index)
            return team
        except Exception as e:
            return {"error": str(e)}