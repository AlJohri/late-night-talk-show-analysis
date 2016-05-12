.PHONY: ratings subtitles

all: ratings subtitles

ratings:
	python scrape_episode_list.py
	python scrape_ratings.py

subtitles:
	python scrape_subtitles.py
	python parse_subtitles.py
