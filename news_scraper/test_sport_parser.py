import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from basic_parser import Main_page_sport_parser, Article_Scraper


class TestSportParser(unittest.TestCase):
    def setUp(self):
        self.main_url = "https://www.espn.com/soccer/"
        self.parser = Main_page_sport_parser(self.main_url)

    @patch('requests.get')
    def test_get_article_links(self, mock_get):
        
        html_content = '''
        <html>
        <body>
            <a href="/soccer/story/12345" class="contentItem__padding contentItem__padding--border">
                <h2 class="contentItem__title contentItem__title--story">Sample Article Title</h2>
            </a>
        </body>
        </html>
        '''
        
        mock_response = MagicMock()
        mock_response.text = html_content
        mock_get.return_value = mock_response

        articles = self.parser.get_article_links()
        expected_result = [{'title': 'Sample Article Title', 'url': 'https://www.espn.com/soccer/+ /soccer/story/12345'}]

        self.assertEqual(articles, expected_result)

    @patch('requests.get')
    def test_get_article_content(self, mock_get):
        
        html_content = '''
        <html>
        <body>
            <div class="timestamp">2024-11-11</div>
            <div class="article-body">
                <h2>Introduction</h2>
                <p>This is the first paragraph of the introduction.</p>
                <h2>Main Content</h2>
                <p>This is the first paragraph of the main content.</p>
                <p>This is the second paragraph of the main content.</p>
            </div>
        </body>
        </html>
        '''
        
        mock_response = MagicMock()
        mock_response.text = html_content
        mock_get.return_value = mock_response

        article_url = "https://www.espn.com/soccer/story/12345"
        scraper = Article_Scraper(self.main_url)
        article_content = scraper.get_article_content(article_url)

        expected_content = {
            'timestamp': '2024-11-11',
            'sections': [
                {
                    'title': 'Introduction',
                    'content': ['This is the first paragraph of the introduction.']
                },
                {
                    'title': 'Main Content',
                    'content': [
                        'This is the first paragraph of the main content.',
                        'This is the second paragraph of the main content.'
                    ]
                }
            ]
        }

        self.assertEqual(article_content, expected_content)


if __name__ == '__main__':
    unittest.main()
