.PHONY: ratings subtitles

all: ratings subtitles

ratings:
	python scraper/scrape_episode_list.py
	python scraper/scrape_ratings.py

subtitles:
	python scraper/scrape_subtitles.py
	python scraper/parse_subtitles.py
