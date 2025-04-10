from database.models import GamesStatuses
from database.session import SessionLocal
from typing import Dict
from cachetools import TTLCache
from database.postgres.dto import TeamDTO, CountryDTO, LeagueDTO, GameDTO, SportDTO, PlayerDTO
from database.postgres.dal import TeamDAL, LeagueDAL, GameDAL, CountryDAL, SportDAL, PlayerDal
from datetime import datetime

status_cache = TTLCache(maxsize=10, ttl=60*60*24)

TEAMS = 'teams'
LEAGUES = 'leagues'
GAMES = ["games", "fixtures", "fights", "races", "competitions"]
GAME = 'game'
FIXTURE = 'fixture'
SPORT_TO_SAVE_TEAM_AS_LEAGUE = ['mma', 'formula-1']
PLAYERS = ['fighters', 'drivers', 'players']
CUSTOM_GAMES = {
    'cancelled': ['Cancelled', 'Suspended'],
    'finished': ['Finished', 'Awarded', 'After Over Time', 'Completed', 'After Extra Time', 'After Penalties', 'Completed'],
    'abandoned': ['Abandoned', 'Interrupted'],
    'postponed': ['Postponed'],
    'scheduled': ['Not Started', 'Time To Be Defined', 'Scheduled'],
    'not_played': ['Technical Loss', 'WalkOver'],

}
MMA_LOGO = "https://www.api-football.com/public/img/home1/mma-logo.png"

IN_PROGRESS = 'play'

def save_api_data(json_data: Dict, sport_name: str) -> None:
    session = SessionLocal()
    try:
        sport_dal = SportDAL(session)
        sport_entry = sport_dal.get_sport_by_name(sport_name)
        if sport_entry:
            sport_id = sport_entry.sport_id
        else:
            sport_dto = SportDTO(sport_name=sport_name)
            sport_id = sport_dal.create_sport(sport_dto).sport_id


        entity = json_data.get("get")
        json_data_response = json_data.get("response", [])

        country_dal = CountryDAL(session)

        if entity == TEAMS:
            league_api_id=None
            league_id=None

            parameters = json_data.get('parameters', [])
            if (isinstance(parameters, list) and len(parameters) > 0) or isinstance(parameters, dict):
                league_api_id = json_data.get('parameters').get('league')

            if league_api_id:
                league_dal = LeagueDAL(session)
                league_entry = league_dal.get_league_by_api_id_and_sport_id(int(league_api_id), sport_id)
                if league_entry:
                    league_id = league_entry.league_id
            process_entity_teams(json_data_response, sport_id, session, league_id)
            if sport_name in SPORT_TO_SAVE_TEAM_AS_LEAGUE:
                process_entity_leagues(json_data_response, sport_id, country_dal, session)

        elif entity == LEAGUES:
            process_entity_leagues(json_data_response, sport_id, country_dal, session)

        elif entity in GAMES:
            game_dal = GameDAL(session)
            team_dal = TeamDAL(session)
            league_dal = LeagueDAL(session)
            game_dto_list = []
            for game in json_data_response:

                if FIXTURE in game or GAME in game:
                    separated_data = game.get(FIXTURE) or game.get(GAME)
                    api_id = separated_data.get("id")
                    date = separated_data.get("date")
                    status = separated_data.get('status')
                else:
                    api_id = game.get('id')
                    date = game.get('date')
                    status = game.get('status')


                if isinstance(date, dict):
                    time = date.get('time')
                    date = date.get('date')
                else:
                    time = game.get('time')

                try:
                    if isinstance(date, str):
                        parsed_date = datetime.fromisoformat(date)
                    elif isinstance(date, datetime):
                        parsed_date = date
                    else:
                        raise ValueError("Unknown format of date")

                    date = parsed_date.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"error processing date data: {e}")
                    date = None

                if isinstance(status, dict):
                    status = status.get('long', '')

                if not isinstance(status, str) or not status:
                    status = IN_PROGRESS

                status_lower = status.lower()
                game_type_result = None
                for game_type, phrases in CUSTOM_GAMES.items():
                    if any(phrase in status_lower for phrase in map(str.lower, phrases)):
                        game_type_result = game_type
                        break

                if not game_type_result:
                    game_type_result = IN_PROGRESS

                if game_type_result in status_cache:
                     status_entry = status_cache[game_type_result]
                else:
                    status_entry = session.query(GamesStatuses).filter_by(status=game_type_result).first()

                    if not status_entry:
                        status_entry = GamesStatuses(status=game_type_result)
                        session.add(status_entry)
                        session.commit()

                        status_cache[game_type_result] = status_entry

                game_status_id = status_entry.game_status_id

                country_entry = game.get('location').get('country') if 'location' in game else game.get('country')
                if country_entry:
                    country_id = save_country_and_get_id(country_entry, country_dal)


                league_entry = game.get('league')
                if league_entry:
                    process_entity_leagues([league_entry], sport_id, country_dal, session)
                    league_id = league_dal.get_league_by_name_and_sport_id(league_entry.get('name') or league_entry, sport_id).league_id


                teams_data = game.get('teams', {})
                if teams_data:
                    team_away_data = teams_data.get('away', {}) or teams_data.get('visitors', {})
                    team_home_data = teams_data.get('home', {})
                    process_entity_teams([team_away_data, team_home_data], sport_id, session)
                    team_away_id = team_dal.get_team_by_name_and_sport_id(team_away_data.get('name'), sport_id).team_index_id
                    team_home_id = team_dal.get_team_by_name_and_sport_id(team_home_data.get('name'), sport_id).team_index_id


                scores_data = game.get('scores', {}) or game.get('goals', {})
                if scores_data:
                    score_away_data = scores_data.get('away') or scores_data.get('visitors')
                    score_home_data = scores_data.get('home')
                    if not isinstance(score_home_data, int) and isinstance(score_home_data, dict):
                        score_home_data = score_home_data.get('points') or score_home_data.get('total')
                    if not isinstance(score_away_data, int) and isinstance(score_away_data, dict):
                        score_away_data = score_away_data.get('points') or score_away_data.get('total')

                game_dto = GameDTO(league_id=league_id if league_entry else None,
                                   sport_id=sport_id,
                                   country_id=country_id if country_entry else None,
                                   team_away_id=team_away_id or None,
                                   team_home_id=team_home_id or None,
                                   score_away_team=score_away_data or None,
                                   score_home_team=score_home_data or None,
                                   status=status,
                                   game_status=game_status_id or None,
                                   time=time,
                                   date=date,
                                   api_id=api_id)
                game_dto_list.append(game_dto)
            game_dal.save_games(game_dto_list)

        elif entity in PLAYERS:
            team_api_id = None

            parameters = json_data.get('parameters', [])
            if (isinstance(parameters, list) and len(parameters) > 0) or isinstance(parameters, dict):
                team_api_id = json_data.get('parameters').get('team')

            process_entity_players(json_data_response, sport_id, session, team_api_id)


    except Exception as e:
        session.rollback()
        print("data was screwed up")
        print(f"error processing data: {e}")


def save_country_and_get_id(country_entry, country_dal: CountryDAL) -> int:
    if not country_entry:
        return None
    if isinstance(country_entry, str):
        country_entry = {'name': country_entry}

    country_dto = CountryDTO(name=country_entry.get('name'),
                                 code=country_entry.get('code'),
                                 flag=country_entry.get('flag'),
                                 api_id=country_entry.get('id'))
    country_dto.name=country_dto.name.replace('-',' ')
    return country_dal.save_country(country_dto)

def process_entity_teams(json_data, sport_id: int, session: SessionLocal, league_id=None):
    team_dal = TeamDAL(session)
    team_dto_list = []


    for team in json_data:
        if sport_id == 10:
            team_bad_logo_info = team.get('logo', {})
            team_bad_photo_info = team.get('photo', {})
        else:
            team_bad_logo_info, team_bad_photo_info = True, True

        team_dto = TeamDTO(sport_id=sport_id,
                           name=team.get('name') or team.get('team').get('name'),
                           logo=team.get('logo') or team.get('photo') or team.get('team').get('logo') or team.get('team').get('photo') if team_bad_logo_info or team_bad_photo_info else MMA_LOGO,
                           api_id=team.get('id') or team.get('team').get('id'),
                           league_id=league_id)
        team_dto_list.append(team_dto)
    team_dal.save_teams(team_dto_list)

def process_entity_leagues(json_data, sport_id: int, country_dal: CountryDAL, session: SessionLocal):
    league_dal = LeagueDAL(session)
    league_dto_list = []
    for league in json_data:
        country_id = save_country_and_get_id(league.get('country'), country_dal)
        if isinstance(league, str):
            league = {'name': league}
        league_dto = LeagueDTO(name=league.get('name'),
                               logo=league.get('logo'),
                               sport_id=sport_id,
                               api_id=league.get('id'),
                               country=country_id)
        league_dto_list.append(league_dto)
    league_dal.save_leagues(league_dto_list)

def process_entity_players(json_data, sport_id: int, session: SessionLocal, team_id=None):
    player_dal = PlayerDal(session)
    team_dal = TeamDAL(session)
    players_dto_list = []

    team = None
    if team_id:
        team = team_dal.get_team_by_api_id_and_sport_id(team_id, sport_id)

    for player_entry in json_data:
        player_info = player_entry.get("player", player_entry)
        if not player_info:
            continue

        player_team = None
        if not team_id:
            team_data = player_info.get("team")
            if isinstance(team_data, list) and team_data:
                team_api_id = team_data[0].get("id")
            elif isinstance(team_data, dict):
                team_api_id = team_data.get("id")
            else:
                team_api_id = None

            if team_api_id:
                player_team = team_dal.get_team_by_api_id_and_sport_id(team_api_id, sport_id)

        player_dto = PlayerDTO(
            name=player_info.get("name"),
            logo=player_info.get("photo") or player_info.get("image"),
            sport_id=sport_id,
            api_id=player_info.get("id"),
            team_index_id=team.team_index_id if team else (player_team.team_index_id if player_team else None)
        )
        players_dto_list.append(player_dto)

    player_dal.save_players(players_dto_list)