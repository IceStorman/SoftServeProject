import requests
from bs4 import BeautifulSoup
import time



class Main_page_sport_parser:
    def __init__(self, main_url):
        self.main_url = main_url

    def get_article_links(self):
        response = requests.get(self.main_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        for link in soup.find_all('a', class_="contentItem__padding contentItem__padding--border"):
            article_url = link['href']
            title = link.find('h2', class_='contentItem__title contentItem__title--story').get_text()
            articles.append({'title':title,
                             'url':article_url
                             })
        return articles




class Article_Scraper(Main_page_sport_parser):
    def get_article_content(self, article_url):
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = []
        elements = soup.find_all(['h2','p','ul'])
        current_section = None 
        for element in elements:
            if element.name == 'h2':
                if current_section:
                    sections.append(current_section)
                current_section = {'title': element.get_text(), 'content':[]}

            elif element.name in ['p', 'ul']:
                if current_section:
                    current_section['content'].append(element.get_text())

        if current_section:
            sections.append(current_section) 

        
