from service.api_logic.games_logic import get_stream_info_today, get_stream_info_for_sport
from database.session import SessionLocal

session=SessionLocal()

board = get_stream_info_today(session)
print (board)