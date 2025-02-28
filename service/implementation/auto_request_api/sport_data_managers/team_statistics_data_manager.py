from typing import Dict, Optional
from database.models import Sport
from database.session import SessionLocal
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_team_statistics_url, \
    get_team_statistics_index, get_host
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager


class TeamStatisticsDataManager(AbstractSportDataManager):
    _sport_id: Optional[int]
    _team_id: Optional[int]
    _league_id: Optional[int]

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

    def get_teams_statistics(self) -> Dict[str, str]:
        url = get_team_statistics_url(self._sport_name, self._team_id, self._league_id)
        index = get_team_statistics_index(self._sport_name, self._team_id, self._league_id)

        return self._try_return_json_data(url, index)