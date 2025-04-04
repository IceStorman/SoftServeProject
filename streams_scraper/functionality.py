from database.session import SessionLocal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class GameScraper:
    def __init__(self):
        self.session = SessionLocal()
        self.driver = self._initialize_webdriver()
        self.games = []
        self.future_games = []

    @staticmethod
    def _initialize_webdriver():
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
        return driver

    def fetch_games(self):
        self.games = get_games_today(session=self.session)

    def filter_future_games(self):
        self.future_games = [
            f"{game['home_team_name']} vs {game['away_team_name']} {game['date']}"
            for game in self.games if game['status'] == 'Not Started'
        ]

    def search_game_links(self):
        links = []
        base_url = "https://www.google.com/search"

        for game in self.future_games:
            search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
            self.driver.get(search_url)
            results = self.driver.find_elements(By.CLASS_NAME, 'LC20lb MBeuO DKV0Md')[:3]
            game_links = [result.text for result in results]
            links.append({
                'game': game,
                'links': game_links
            })
        return links

    def run(self):
        self.fetch_games()
        self.filter_future_games()
        links = self.search_game_links()
        print("Future Games:", self.future_games)
        print("Links:", links)


