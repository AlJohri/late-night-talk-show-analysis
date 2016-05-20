.PHONY: data subtitles

data: subtitles imdb comedy_central_metadata

subtitles:
	python scripts/scrape_subtitles.py
	python scripts/parse_subtitles.py

imdb:
	python scripts/scrape_imdb.py

comedy_central_metadata:
	python scripts/scrape_comedy_central_metadata.py

gist:
	gist --update https://gist.github.com/31ce93ae800552e844448d80cc7353fe analysis/analysis.ipynb
	open "http://nbviewer.jupyter.org/gist/AlJohri/31ce93ae800552e844448d80cc7353fe"
