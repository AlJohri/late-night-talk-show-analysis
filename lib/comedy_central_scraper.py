import requests, csv

def scrape_comedy_central(url):

    fieldnames = [
        'id',
        'episode_number',
        'episode_airing_order',
        'title',
        'air_date',
        'canonical_url',
        'content_rating',
        'description',
        'duration',
        'image',
        'publish_date',
        'views',
        'imdb_url',
        'season_id',
        'season_number',
        'season_title',
        'series_id',
        'series_title',
    ]

    with open("data/comedy_central_metadata.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()

    page = 1

    while True:
        print("downloading page %d..." % page)
        response = requests.get(url % page)
        print(url % page)
        print(response.status_code)
        print(response.content) # doesn't work anymore
        data = response.json()
        if len(data['result']['items']) == 0: break

        for item in data['result']['items']:

            assert(len(item['images']) <= 1)

            imdb_urls = [link for link in item['showAdditionalLinks'] if link['linkType'] == "imdb"] if item.get('showAdditionalLinks') else []

            row = {
                'id': item['id'],
                'episode_number': item['season']['episodeNumber'],
                'episode_airing_order': item['episodeAiringOrder'],
                'title': item['title'],
                'air_date': item['airDate'],
                'canonical_url': item['canonicalURL'],
                'content_rating': item['contentRating'],
                'description': item['description'],
                'duration': item['duration'],
                'image': item['images'][0]['url'] if len(item['images']) == 1 else "",
                'publish_date': item['publishDate'],
                'views': item['views'],
                'imdb_url': imdb_urls[0]['url'] if imdb_urls else "",
                'season_id': item['season']['id'],
                'season_number': item['season']['seasonNumber'],
                'season_title': item['season']['title'],
                'series_id': item['show']['id'],
                'series_title': item['show']['title'],
            }

            print(row['id'], row['season_number'], row['episode_number'], row['title'])

            with open("data/comedy_central_metadata.csv", "a") as f:
                writer = csv.DictWriter(f, fieldnames)
                writer.writerow(row)

        page += 1
