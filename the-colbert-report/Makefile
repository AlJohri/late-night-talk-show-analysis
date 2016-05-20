.PHONY: data subtitles

data: subtitles imdb

subtitles:
	python scripts/scrape_subtitles.py
	python scripts/parse_subtitles.py

imdb:
	python scripts/scrape_imdb.py

comedy_central_metadata:
	python scripts/scrape_comedy_central_metadata.py

gist:
	gist --update https://gist.github.com/cfcad84b3922922fef837d45c19b31df
	open "http://nbviewer.jupyter.org/gist/AlJohri/cfcad84b3922922fef837d45c19b31df"
