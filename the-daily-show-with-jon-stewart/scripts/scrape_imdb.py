import logging, os
from lib.imdb_scraper import IMDBScraper
from settings import IMDB_SERIES_ID

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.WARN)

imdb_scraper = IMDBScraper(IMDB_SERIES_ID)

if not os.path.exists("data/imdb_episode_list.csv"):
    episodes = []
    for season in range(1, 20+1):
        season_episodes = imdb_scraper.scrape_episode_list(season)
        episodes += season_episodes
    imdb_scraper.save_episode_list(episodes)
else:
    episodes = imdb_scraper.read_episode_list()

if not os.path.exists("data/imdb_ratings.csv"):
    ratings = imdb_scraper.scrape_ratings(episodes)
    imdb_scraper.save_ratings(ratings)