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

        
        
        timestamp = soup.select_one('.timestamp')

        article_data = {
            
            'timestamp': timestamp.get_text(strip=True) if timestamp else None,
            'sections': []
        }

        
        content_div = soup.select_one('.article-body')
        if content_div:
            paragraphs = content_div.find_all(['p', 'h2'])

            current_section = None
            for element in paragraphs:
                if element.name == 'h2':
                    if current_section:
                        article_data['sections'].append(current_section)
                    current_section = {
                        'title': element.get_text(strip=True),
                        'content': []
                    }
                elif element.name == 'p':
                    if current_section is None:
                        
                        current_section = {'title': '', 'content': []}
                    current_section['content'].append(element.get_text(strip=True))

            
            if current_section:
                article_data['sections'].append(current_section)

        time.sleep(1)

        return article_data

        
