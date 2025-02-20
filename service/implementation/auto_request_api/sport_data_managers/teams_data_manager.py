from typing import Optional, Dict

from database.models import Sport
from database.session import SessionLocal
from dto.api_input import TeamsLeagueDTO
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_team_statistics_url, \
    get_team_statistics_index, get_host, get_team_index


class TeamsDataManager(AbstractSportDataManager):
    _teams__sport_id: Optional[int]
    _leagues__api_id: Optional[int]
    _countries__api_id: Optional[int]
    _page_number: Optional[int]
    _elements_per_page: Optional[int]

    def __init__(self, new_data):
        super().__init__(new_data)
        query = (
            SessionLocal().query(
                Sport.sport_id,
                Sport.sport_name
            )
            .filter(Sport.sport_id == new_data.teams__sport_id)
        )

        ix = query.first()
        if ix is not None:
            self._sport_name = ix.sport_name

        self._leagues__api_id = new_data.leagues__api_id
        self._host = get_host(self._sport_name)

        self._page_number = new_data.page
        self._elements_per_page = new_data.per_page

    def get_teams_data(self, pagination):
        index = get_team_index(self._sport_name, self._leagues__api_id)
        result = get_teams(self._data_dict, pagination)
        if result:
            return result
        url_first = get_host(self._sport_name)
        url = "https://"+url_first+"/"+index.replace("teams/","")
        try:
            team = self._try_return_json_data(url, index)
            return team
        except Exception as e:
            return {"error": str(e)}