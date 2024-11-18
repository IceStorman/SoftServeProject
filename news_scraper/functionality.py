from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
import json

class Main_page_sport_parser:
    def __init__(self, main_url):
        self.main_url = main_url

    def get_article_links(self, max_articles=5):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(self.main_url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching the page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        for first_div in soup.find_all('div', class_='interior secondary'):
            first_section = first_div.find('section', {'id': 'pane-main'})
            if first_section:
                secondary_section = first_section.find('section', {'id': 'main-container'})
                if secondary_section:
                    second_div = secondary_section.find('div', class_='main-content layout-dbc one-feed')
                    if second_div:
                        third_section = second_div.find('section', {'id': 'news-feed'})
                        if third_section:
                            fourth_sections = third_section.find_all('section', class_='contentItem contentItem--collection')
                            for fourth_section in fourth_sections:
                                fifth_section = fourth_section.find('section', class_='contentItem__content contentItem__content--story has-image has-video contentItem__content--collection contentItem__content--enhanced contentItem__content--fullWidth')
                                if fifth_section:
                                    a_tag = fifth_section.find('a', class_='contentItem__padding contentItem__padding--border')
                                    if a_tag:
                                        article_url_suffix = a_tag.get('href')
                                        third_div = a_tag.find('div', class_='contentItem__contentWrapper')
                                        if third_div:
                                            fourth_div = third_div.find('div', class_='contentItem__titleWrapper')
                                            if fourth_div:
                                                title_tag = fourth_div.find('h2', class_='contentItem__title contentItem__title--story')

                                                if article_url_suffix and title_tag:
                                                    title = title_tag.get_text()
                                                    full_url = urljoin(self.main_url, article_url_suffix)
                                                    articles.append({'title': title, 'url': full_url})
                                if len(articles) >= max_articles:
                                    break

        print(f"Found {len(articles)} articles:")
        for article in articles:
            print(f"Title: {article['title']}, URL: {article['url']}")

        return articles

class Article_Scraper(Main_page_sport_parser):

    def get_article_content(self, full_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(full_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching the article. Status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        article_data = {
            'timestamp': None,
            'article': {}
        }

       
        timestamp = soup.select_one('.author .timestamp')
        article_data['timestamp'] = timestamp.get_text(strip=True) if timestamp else article_data['timestamp'] == time.strftime("%Y-%m-%d-%h")
       
        for aside in soup.find_all('aside', class_=['inline editorial float-r', 'inline float-r inline-track']):
            aside.decompose()

        
        content_div = soup.select_one('.article-body')
        if content_div:
            elements = content_div.find_all(['p', 'h2', 'h3', 'img'])
            current_section_title = None
            current_section_content = []
            current_section_images = []
            current_section_subheadings = []  
            section_counter = 1

            for element in elements:
                if element.name == 'h2':  
                    if current_section_title or current_section_content or current_section_images:
                        article_data['article'][f'section_{section_counter}'] = {
                            'title': current_section_title,
                            'subheadings': current_section_subheadings,
                            'content': current_section_content,
                            'images': current_section_images
                            
                        }
                        section_counter += 1

                    
                    current_section_title = element.get_text(strip=True)
                    current_section_content = []
                    current_section_images = []
                    current_section_subheadings = []

                elif element.name == 'h3':  
                    current_section_subheadings.append(element.get_text(strip=True))

                elif element.name == 'p':  
                    current_section_content.append(element.get_text(strip=True))

                elif element.name == 'img' and 'imageLoaded lazyloaded' in element.get('class', []):  
                    image_url = element.get('src')
                    if image_url:
                        article_data['images'].append(image_url)


            
            if current_section_title or current_section_content or current_section_images:
                article_data['article'][f'section_{section_counter}'] = {
                    'title': current_section_title,
                    'content': current_section_content,
                    'images': current_section_images,
                    'subheadings': current_section_subheadings
                }

        time.sleep(1)  
        return article_data



    def print_article(self, article):
        print(f"\n---\nTitle: {article['title']}")
        print(f"URL: {article['url']}")
        content = self.get_article_content(article['url'])

        if not content:
            print("Failed to fetch the content of the article.")
            return

        print(f"Timestamp: {content['timestamp']}\n")

        for section_key, section_data in content['article'].items():
            title = section_data['title']
            paragraphs = section_data['content']
            images = section_data['images']
            subheadings = section_data.get('subheadings', [])

            print(f"Section Title: {title}\n")

            for idx, paragraph in enumerate(paragraphs):
                if idx < len(subheadings) and subheadings[idx]:
                    print(f"Subheading: {subheadings[idx]}\n")

                
                formatted_paragraph = paragraph.replace('<br>', '\n\t')
                print(f"Paragraph Text:\n\t{formatted_paragraph}\n")

            
            if images:
                print("Images in this paragraph:")
                for image in images:
                    print(f"\t{image}")
                print("\n")
            else:
                print("No images in this paragraph.\n")

        print("End of Article\n---")


    



        def write_article_into_json(self, article):
            
            pass