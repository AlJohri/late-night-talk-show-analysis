import os
from lib.comedy_central_scraper import scrape_comedy_central

if not os.path.exists("data/comedy_central_metadata.csv"):
    scrape_comedy_central("http://www.cc.com/feeds/ent_m112_cc/V1_1_1/980d89f3-ccac-4cd7-b463-9208cad3555e/2796e828-ecfd-11e0-aca6-0026b9414f30/?fullEpisodes=0&pageNumber=%d")
else:
    print("data/comedy_central_metadata.csv already exists")