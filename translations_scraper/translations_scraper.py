from service.api_logic.games_logic import get_games_today
from database.session import SessionLocal
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


session = SessionLocal()
options = Options()
arguments = [
    "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
]
for arg in arguments:
    options.add_argument(arg)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

stealth(driver,
languages=["en-US", "en"],
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True)

games = get_games_today(session=session)

future_games = [
    f"{game['home_team_name']} vs {game['away_team_name']}" 
    for game in games if game['status'] == 'Not Started'
]

print(future_games)

for game in future_games:
    base_url = "https://www.google.com/search"
    search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"








