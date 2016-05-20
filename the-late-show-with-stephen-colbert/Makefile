.PHONY: data ratings subtitles notebook gist

data: subtitles imdb

imdb:
	python scripts/scrape_imdb.py

subtitles:
	python scripts/scrape_subtitles.py
	python scripts/parse_subtitles.py

notebook:
	jupyter notebook analysis/analysis.ipynb

gist:
	gist --update https://gist.github.com/3825066ecfa4688c87f61c1a250aa778 analysis/analysis.ipynb
	open "http://nbviewer.jupyter.org/gist/AlJohri/3825066ecfa4688c87f61c1a250aa778"
