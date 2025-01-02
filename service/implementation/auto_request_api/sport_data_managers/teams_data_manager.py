from typing import Optional

from database.session import SessionLocal
from dto.api_input import TeamsLeagueDTO
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_team_statistics_url, \
    get_team_statistics_index, get_host, get_sport_name


class TeamsDataManager(AbstractSportDataManager):
    _teams__sport_id: Optional[int]
    _leagues__api_id: Optional[int]
    _countries__api_id: Optional[int]
    _page: Optional[int]
    _per_page: Optional[int]

    def __init__(self, data_manager):
        super().__init__(data_manager)

        self._teams__sport_id = data_manager.teams__sport_id
        self._host = get_host(self._teams__sport_id)

        self._sport_name = get_sport_name(self._teams__sport_id)

        self._leagues__api_id = data_manager.leagues__api_id
        self._countries__api_id = data_manager.countries__api_id
        self._page = data_manager.page
        self._per_page = data_manager.per_page

    def get_data(self):
        if not self._leagues__api_id:
            return {"error": "Missing or invalid parameters: 'league_id' are required."}
        index = f"teams/teams?league={self._leagues__api_id}"
        result = get_teams(SessionLocal, dto=TeamsLeagueDTO)
        if result is not []:
            return result
        url = f"https://v2.nba.api-sports.io/teams?league={self._leagues__api_id}"
        host = "v2.nba.api-sports.io"
        try:
            team = self.main_request(host, self._sport_name, url, index)
            return team
        except Exception as e:
            return {"error": str(e)}