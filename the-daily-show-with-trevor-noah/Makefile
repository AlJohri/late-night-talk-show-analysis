.PHONY: gist data comedy_central_metadata

data: comedy_central_metadata

comedy_central_metadata:
	python scripts/scrape_comedy_central_metadata.py

gist:
	gist --update https://gist.github.com/b8b1e273078a1e8334288f381bf6f7c6 analysis/analysis.ipynb
	open "http://nbviewer.jupyter.org/gist/AlJohri/b8b1e273078a1e8334288f381bf6f7c6"	
