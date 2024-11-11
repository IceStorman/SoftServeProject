import requests
from bs4 import BeautifulSoup
import time
import json


class Main_page_sport_parser:
    def __init__(self, url):
        self.url = url

    def fetch_page(self, url_suffix=''):
        pass

class Article_Scraper(Main_page_sport_parser):
    def __init__(self, article_url):
        self.article_url = article_url
