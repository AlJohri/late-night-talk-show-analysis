.PHONY: data ratings subtitles notebook gist

data: ratings subtitles

ratings:
	python scraper/scrape_episode_list.py
	python scraper/scrape_ratings.py

subtitles:
	python scraper/scrape_subtitles.py
	python scraper/parse_subtitles.py

notebook:
	jupyter notebook analysis/analysis.ipynb

gist:
	gist --update https://gist.github.com/3825066ecfa4688c87f61c1a250aa778 analysis/analysis.ipynb
	open "http://nbviewer.jupyter.org/gist/AlJohri/3825066ecfa4688c87f61c1a250aa778"
