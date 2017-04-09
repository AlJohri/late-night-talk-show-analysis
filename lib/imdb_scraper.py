import requests, grequests, lxml.html, csv, arrow, logging

from lib.utils import set_meta, handler

class IMDBScraper():

    base_url = "http://www.imdb.com"
    date_format = 'D MMM(.)? YYYY'
    episodes_url = "http://www.imdb.com/title/%s/episodes?season=%d"

    def __init__(self, imdb_id, latest_episode_number=None):
        self.id = imdb_id
        self.latest_episode_number = latest_episode_number

    def scrape_episode_list(self, season):
        response = requests.get(self.episodes_url % (self.id, season))
        doc = lxml.html.fromstring(response.content)

        tv_season = doc.cssselect("div[itemtype='http://schema.org/TVSeason']")[0]
        number_of_episodes = int(tv_season.cssselect('meta[itemprop=numberofEpisodes]')[0].get('content'))

        rows = []

        for tv_episode in tv_season.cssselect("div[itemtype='http://schema.org/TVEpisode']"):

            episode_dict = {
                "season": season,
                "episode_number": int(tv_episode.cssselect("meta[itemprop='episodeNumber']")[0].get('content')),
                "air_date": tv_episode.cssselect("div.airdate")[0].text.strip(),
                "url": tv_episode.cssselect("a[itemprop='name']")[0].get('href'),
                "name": tv_episode.cssselect("a[itemprop='name']")[0].text,
                "description": tv_episode.cssselect("div[itemprop='description']")[0].text_content().strip(),
            }

            msg = " ".join([str(season), str(episode_dict['episode_number']).rjust(3), episode_dict['air_date'], episode_dict['url'], episode_dict['name']])

            if self.latest_episode_number and episode_dict['episode_number'] > self.latest_episode_number:
                logging.debug("skipping " + msg)
                continue

            try:
                episode_dict['air_date'] = arrow.get(episode_dict['air_date'], self.date_format).strftime("%x") if episode_dict['air_date'] else ""
            except arrow.parser.ParserError:
                logging.error("error parsing date %s" % episode_dict['air_date'])
                episode_dict['air_date'] = None

            episode_dict['url'] = self.base_url + episode_dict['url'].split("?")[0]
            episode_dict['description'] = episode_dict['description'] if episode_dict['description'] != "Add a Plot" else ""

            rows.append(episode_dict)
            logging.debug(msg)

        return rows

    def read_episode_list(self):
        with open("data/imdb_episode_list.csv") as f:
            reader = csv.DictReader(f)
            episodes = [row for row in reader]
        return episodes

    def save_episode_list(self, rows):
        with open("data/imdb_episode_list.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=['season', 'episode_number', 'air_date', 'url', 'name', 'description'])
            writer.writeheader()
            writer.writerows(rows)

    def scrape_ratings(self, episodes):

        # alternative: http://www.omdbapi.com/?i=tt3697842&Season=1

        def make_req(episode):
            return grequests.get(episode['url'], callback=set_meta({"episode": episode}))

        rows = []

        reqs = (make_req(episode) for episode in episodes)
        for response in grequests.imap(reqs, exception_handler=handler):
            doc = lxml.html.fromstring(response.content)
            rating, rating_count = "N/A", "N/A"
            if not doc.cssselect('div.notEnoughRatings'):
                rating = float(doc.cssselect("span[itemprop='ratingValue']")[0].text)
                rating_count = int(doc.cssselect("span[itemprop='ratingCount']")[0].text)
            row = {
                'season': int(response.meta['episode']['season']),
                'episode_number': int(response.meta['episode']['episode_number']),
                'rating': rating,
                'rating_count': rating_count
            }
            msg = " ".join([str(row['season']), str(row['episode_number']), str(row['rating']), str(row['rating_count'])])
            logging.debug(msg)
            rows.append(row)

        rows.sort(key=lambda x: (x['season'], x['episode_number']))

        return rows

    def save_ratings(self, rows):
        with open("data/imdb_ratings.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=['season', 'episode_number', 'rating', 'rating_count'])
            writer.writeheader()
            writer.writerows(rows)
