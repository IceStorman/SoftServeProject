from typing import Optional
from database.models import Sport
from database.session import SessionLocal
from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import \
    AbstractSportDataManager
from service.implementation.auto_request_api.sport_data_managers.sport_consts import get_players_index, get_players_url, get_host


class PlayersDataManager(AbstractSportDataManager):
    _team_id: Optional[int]
    _league_id: Optional[int]
    _search: Optional[str]

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

    def get_data(self):
        index = get_players_index(self._sport_name, self._team_id, self._league_id, self._search)
        url = get_players_url(self._sport_name, self._team_id, self._league_id, self._search)

        try:
            team = self._return_specific_json_data(url, index)
            return team
        except Exception as e:
            return {"error": str(e)}