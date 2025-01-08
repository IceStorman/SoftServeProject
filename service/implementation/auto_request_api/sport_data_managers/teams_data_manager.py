from typing import Optional

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
    _page: Optional[int]
    _per_page: Optional[int]

    def __init__(self, data_manager):
        super().__init__(data_manager)
        query = (
            SessionLocal().query(
                Sport.sport_id,
                Sport.sport_name
            )
            .filter(Sport.sport_id == data_manager.get("teams__sport_id"))
        )

        ix = query.first()
        if ix is not None:
            self._teams__sport_id = ix.sport_name
        #self._teams__sport_id = data_manager.get("teams__sport_id")
        self._leagues__api_id = data_manager.get("leagues__api_id")
        self._host = get_host(self._teams__sport_id)

        #self._sport_name = get_sport_name(self._teams__sport_id)

        #self._countries__api_id = data_manager.get("countries__api_id")
        self._page = data_manager.get("page")
        self._per_page = data_manager.get("per_page")

    def get_teams_data(self, pagination):
        index = get_team_index(self._teams__sport_id, self._leagues__api_id)
        result = get_teams(self._data_dict, pagination)
        if result.get('teams'):
            return result
        url_first = get_host(self._teams__sport_id)
        url = "https://"+url_first+"/"+index.replace("teams/","")
        try:
            team = self.main_request(self._host, self._teams__sport_id, url, index)
            result_again = get_teams(self._data_dict, pagination)
            if result_again.get('teams'):
                return result_again
            return team
        except Exception as e:
            return {"error": str(e)}