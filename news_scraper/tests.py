from basic_parser import  Main_page_sport_parser, Article_Scraper

main_url = "https://www.espn.com/soccer/"

main_page =  Main_page_sport_parser(main_url)
articles = main_page.get_article_links()

article_scraper = Article_Scraper(main_url)

for article in articles[:2]:
    title = article['title']
    url = article['url']
    
    print(f"Заголовок: {title}")
    full_content = article_scraper.get_article_content(url)
    print(f"Контент статті: {full_content}")