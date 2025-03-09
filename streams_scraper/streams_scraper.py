from database.session import SessionLocal
from exept.exeptions import SportNotFoundError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from service.api_logic.games_logic import get_games_today
from api.container.container import Container
from dependency_injector.wiring import Provide, inject
from database.postgres.dto import StreamDTO, StreamStatusDTO, StreamUrlDTO
import re

sport_dal = Provide[Container.sport_dal]

stream_service = Provide[Container.stream_service]


def configure_driver():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )
    return driver


def filter_future_games(games):
    
    return [
        f"{game['home_team_name']} vs {game['away_team_name']} {game['date']}"
        for game in games if game['status'] == 'Not Started'
    ]

def game_name(game):
    return f"{game['home_team_name']} vs {game['away_team_name']}"

def sport_name(url):
    match = re.search(r'api-sports.io/([^/]+)/teams', url)
    return match.group(1) if match else "unknown"


def search_game_links(driver, future_games, games_today):
    
    base_url = "https://www.google.com/search"
    stream_data = []

    for game in future_games:
        search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
        driver.get(search_url)
        links_elements = driver.find_elements(By.CLASS_NAME, 'LC20lb')
        urls = [link.get_attribute('href') for link in links_elements[:3]]

        matching_game = next(
            (g for g in games_today if f"{g['home_team_name']} vs {g['away_team_name']} {g['date']}" == game),
            None
        )
        start_time = matching_game['time'] if matching_game else "Unknown"

        sport_id = "unknown"
        if matching_game:
            team_logo_url = matching_game.get("home_team_logo", "")
            detected_sport_name = sport_name(team_logo_url)  # Використовуємо функцію sport_name
            
            try:
                sport_id = sport_dal.get_sport_by_name(detected_sport_name)
            except SportNotFoundError:
                




#Probillllllllllllllll Probillllllllllllllllllllllll Probillllllllllllllllll
                print(f"Sport '{sport_name}' not found in the database.")
#Probillllllllllllllll Probillllllllllllllllllllllll Probillllllllllllllllll








        stream_dto = StreamDTO(
            title=game_name(game),
            stream_urls=urls if urls else None,
            start_time=start_time,
            sport_id=sport_id
        )
        stream_data.append(stream_dto)

    return stream_data


@inject
def save_stream_data(streams_data):

    stream_service.save_streams_to_streams_table(streams_data)


def main():
    
    session = SessionLocal()
    driver = configure_driver()

    try:
        
        
        games_today = get_games_today()
        future_games = filter_future_games(games_today)

        
        game_data = search_game_links(driver, future_games, games_today, session)

        
        save_stream_data(session, game_data)


    finally:
        driver.quit()
        session.close()


if __name__ == "__main__":
    main()
