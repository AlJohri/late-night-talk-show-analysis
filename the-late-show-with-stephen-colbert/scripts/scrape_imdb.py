from lib.imdb_scraper import IMDBScraper
from settings import IMDB_SERIES_ID, LATEST_EPISODE_NUMBER

season = 1

imdb_scraper = IMDBScraper(IMDB_SERIES_ID, LATEST_EPISODE_NUMBER)
episodes = imdb_scraper.scrape_episode_list(season)
imdb_scraper.save_episode_list(episodes)
ratings = imdb_scraper.scrape_ratings(episodes)
imdb_scraper.save_ratings(ratings)