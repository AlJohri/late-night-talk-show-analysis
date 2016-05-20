.PHONY: data subtitles

data: subtitles imdb

subtitles:
	python scripts/scrape_subtitles.py
	python scripts/parse_subtitles.py

imdb:
	python scripts/scrape_imdb.py

comedy_central_metadata:
	python scripts/scrape_comedy_central_metadata.py
