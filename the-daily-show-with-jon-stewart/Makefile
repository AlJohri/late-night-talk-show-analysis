.PHONY: data subtitles

data: subtitles imdb comedy_central_metadata

subtitles:
	python scripts/scrape_subtitles.py
	python scripts/parse_subtitles.py

imdb:
	python scripts/scripts_imdb.py

comedy_central_metadata:
	python scripts/scrape_comedy_central_metadata.py
