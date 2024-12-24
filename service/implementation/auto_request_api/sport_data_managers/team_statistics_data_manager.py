from typing import Dict, Optional

from dto.api_input import TeamsStatisticsOrPlayersDTO
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_team_statistics_url, get_team_statistics_index
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager


class TeamStatisticsDataManager(AbstractSportDataManager):
    _sport_id: Optional[str]
    _team_id: Optional[int]
    _league_id: Optional[int]

    def __init__(self, team_statistics_data: TeamsStatisticsOrPlayersDTO, new_sport_name):
        super().__init__(team_statistics_data, new_sport_name)

        self._sport_id = team_statistics_data.sport_id
        self._team_id = team_statistics_data.team_id
        self._league_id = team_statistics_data.league_id
        print(f"host: {self._host} sport id: {self._sport_id} | team id: {self._team_id} | league id: {self._league_id}")

    def get_teams_statistics(self) -> Dict[str, str]:
        url = get_team_statistics_url(self._sport_name, self._team_id, self._league_id)
        index = get_team_statistics_index(self._sport_name, self._team_id, self._league_id)

        return self.try_return_json_data(url, index)