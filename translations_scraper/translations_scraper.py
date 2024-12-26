from service.api_logic.games_logic import get_games_today
from database.session import SessionLocal
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from service.api_logic.streams_logic import save_json_stream_to_db


def initialize_session():
    return SessionLocal()

def configure_driver():
    options = Options()
    arguments = [
        "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
    ]
    for arg in arguments:
        options.add_argument(arg)

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

def fetch_games_today(session):
    return get_games_today(session=session)

def filter_future_games(games):
    return [
        f"{game['home_team_name']} vs {game['away_team_name']} {game['date']}" 
        for game in games if game['status'] == 'Not Started'
    ]

def search_game_links(driver, future_games):
    base_url = "https://www.google.com/search"
    for game in future_games:
        search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
        links = driver.find_elements(By.CLASS_NAME, 'LC20lb MBeuO DKV0Md')[:3]
        print(f"Links for {game}: {links}")

def main():
    session = initialize_session()
    driver = configure_driver()

    try:
        games = fetch_games_today(session)
        future_games = filter_future_games(games)
        print(f"Future games: {future_games}")
        
        search_game_links(driver, future_games)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
