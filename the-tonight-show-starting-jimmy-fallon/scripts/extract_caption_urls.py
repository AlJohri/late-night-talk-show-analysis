#!/usr/bin/env python3

import json
import requests
import lxml.html

print('Loading caption urls')
try:
    with open('data/caption_urls.json') as f:
        caption_urls = json.load(f)
except Exception as e:
    caption_urls = {}

print("loaded", len(caption_urls), "caption urls")

with open('data/nbc_metadata.json') as f:
    metadata = json.load(f)
    print("length", len(metadata))
    for id_, episode in sorted(metadata.items(),
        key=lambda x: (
            int(x[1]['attributes']['seasonNumber']),
            int(x[1]['attributes']['episodeNumber'] or -1),)):

        if not episode['attributes']['episodeNumber']:
            print('no episode number????')

        print(episode['attributes']['airdate'],
              episode['attributes']['seasonNumber'],
              (episode['attributes']['episodeNumber'] or "").ljust(3),
              episode['attributes']['title'])

        url = "http://" + episode['attributes']['embedUrl'].lstrip('//')

        try:
            response = requests.get(url)
            doc = lxml.html.fromstring(response.content)
            caption_url = doc.cssselect('meta[property=og\:image]')[0].get('content').replace('.jpg', '.tt').replace('/image/', '/caption/')
            print(caption_url)
        except Exception as e:
            print(e)

        caption_urls[id_] = caption_url

print('Saving caption urls')
with open('data/caption_urls.json', 'w') as f:
    json.dump(caption_urls, f, indent=4)
