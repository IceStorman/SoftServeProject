from functionality import Main_page_sport_parser, Article_Scraper

sport_urls = {
    'main_formula_1_url' : 'https://www.espn.com/f1/',
   ' main_football_url' : 'https://www.espn.com/soccer/',
   ' main_afl_url' : '',
   ' main_baseball_url' : 'https://www.espn.com/mlb/',
    'main_basketball_url' : '',
    
    'main_handball_url' : '',
    'main_hockey_url' : 'https://www.espn.com/nhl/',
    'main_mma_url' : 'https://www.espn.com/mma/',
    'main_nba_url' : 'https://www.espn.com/nba/',
    'main_nfl_url' : 'https://www.espn.com/nfl/',
    'main_rugby_url' : 'https://www.espn.com/rugby/',
    'main_volleyball_url' : ''
}




for url in sport_urls.values():
    if not url.strip():  
        print("Skipping empty URL.")
        continue

    parser = Article_Scraper(url)
    articles = parser.get_article_links(max_articles=3)
    if articles:
        for article in articles:
            content = parser.get_article_content(article['url'])
            if content:
                parser.write_article_into_json(article)
                article_text = "\n".join(
                    " ".join(section['content']) for section in content['article'].values()
                )
            else:
                print("Failed to fetch the content of the article.")
    else:
        print("No articles found.")
