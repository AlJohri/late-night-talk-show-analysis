import requests, lxml.html, csv, arrow

from settings import LATEST_EPISODE_NUMBER

IMDB_BASE_URL = "http://www.imdb.com"
IMDB_SERIES_ID = "tt3697842"

date_format = 'D MMM(.)? YYYY'

url = "http://www.imdb.com/title/%s/episodes" % IMDB_SERIES_ID
response = requests.get(url)
doc = lxml.html.fromstring(response.content)

tv_season = doc.cssselect("div[itemtype='http://schema.org/TVSeason']")[0]
number_of_episodes = int(tv_season.cssselect('meta[itemprop=numberofEpisodes]')[0].get('content'))

rows = []

for tv_episode in tv_season.cssselect("div[itemtype='http://schema.org/TVEpisode']"):

    episode_dict = {
        "number": int(tv_episode.cssselect("meta[itemprop='episodeNumber']")[0].get('content')),
        "airdate": tv_episode.cssselect("div.airdate")[0].text.strip(),
        "url": tv_episode.cssselect("a[itemprop='name']")[0].get('href'),
        "name": tv_episode.cssselect("a[itemprop='name']")[0].text,
        "description": tv_episode.cssselect("div[itemprop='description']")[0].text_content().strip(),
    }

    if episode_dict['number'] > LATEST_EPISODE_NUMBER:
        print("skipping", episode_dict)
        continue

    episode_dict['airdate'] = arrow.get(episode_dict['airdate'], date_format).strftime("%x") if episode_dict['airdate'] else ""
    episode_dict['url'] = IMDB_BASE_URL + episode_dict['url'].split("?")[0]
    episode_dict['description'] = episode_dict['description'] if episode_dict['description'] != "Add a Plot" else ""

    rows.append(episode_dict)
    print(str(episode_dict['number']).rjust(3), episode_dict['airdate'], episode_dict['url'], episode_dict['name'])

with open("data/episode_list.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=['number', 'airdate', 'url', 'name', 'description'])
    writer.writeheader()
    writer.writerows(rows)
