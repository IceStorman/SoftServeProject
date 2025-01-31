from typing import Dict, Optional
from database.postgres.dal.sport import SportDAL
from database.models import Sport
from database.session import SessionLocal
from dto.api_input import TeamsStatisticsOrPlayersDTO
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_team_statistics_url, \
    get_team_statistics_index, get_host
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager


class TeamStatisticsDataManager(AbstractSportDataManager):
    _sport_id: Optional[int]
    _team_id: Optional[int]
    _league_id: Optional[int]

    def __init__(self, team_statistics_data: Dict):
        super().__init__(team_statistics_data)

        self._host = get_host(self._sport_name)

        self._team_id = team_statistics_data.get("team_id")
        self._league_id = team_statistics_data.get("league_id")

    def get_teams_statistics(self) -> Dict[str, str]:
        url = get_team_statistics_url(self._sport_name, self._team_id, self._league_id)
        index = get_team_statistics_index(self._sport_name, self._team_id, self._league_id)

        return self.try_return_json_data(url, index)