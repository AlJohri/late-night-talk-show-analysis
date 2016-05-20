import os
from lib.comedy_central_scraper import scrape_comedy_central

if not os.path.exists("data/comedy_central_metadata.csv"):
    scrape_comedy_central("http://www.cc.com/feeds/ent_m112_cc/V1_1_1/980d89f3-ccac-4cd7-b463-9208cad3555e/7c2d44b4-c8b1-43a9-9bfc-32af988eab20/?fullEpisodes=0&pageNumber=%d")
else:
    print("data/comedy_central_metadata.csv already exists")