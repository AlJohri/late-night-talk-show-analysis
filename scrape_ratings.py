import csv, grequests, lxml.html

# alternative: http://www.omdbapi.com/?i=tt3697842&Season=1

from utils import set_meta, handler

def make_req(episode):
    return grequests.get(episode['url'], callback=set_meta({"episode_number": episode['number']}))

with open("data/episode_list.csv") as f:
    reader = csv.DictReader(f)
    episodes = [row for row in reader]

rows = []

# TODO scrape "table.cast_list"

reqs = (make_req(episode) for episode in episodes)
for response in grequests.imap(reqs, exception_handler=handler):
    doc = lxml.html.fromstring(response.content)
    rating, rating_count = "N/A", "N/A"
    if not doc.cssselect('div.notEnoughRatings'):
        rating = float(doc.cssselect("span[itemprop='ratingValue']")[0].text)
        rating_count = int(doc.cssselect("span[itemprop='ratingCount']")[0].text)
    row = {"number": int(response.meta['episode_number']), "rating": rating, 'rating_count': rating_count}
    print(row['number'], row['rating'], row['rating_count'])
    rows.append(row)

rows.sort(key=lambda x: x['number'])

with open("data/ratings.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=['number', 'rating', 'rating_count'])
    writer.writeheader()
    writer.writerows(rows)