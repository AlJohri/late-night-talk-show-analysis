#!/usr/bin/env python3

import os
import json
import requests
from youtube_dl import YoutubeDL

print("Loading video segment ids...")

video_ids = set()
for filename in os.listdir('data/archive/parsed/'):
    with open(f'data/archive/parsed/{filename}') as f:
        video_ids |= set(json.load(f)['video_ids'])

print(f"Loaded {len(video_ids)} video segment ids...")

yd = YoutubeDL()

for id_ in video_ids:

    print(f'Downloading metadata for {id_}')
    url = f'http://video.foxnews.com/v/{id_}/'
    info = yd.extract_info(url, download=False, ie_key='FoxNews', process=False)
    with open(f'data/metadata/parsed/{id_}.json', 'w') as f:
        json.dump(info, f, indent=4)
    assert len(info['subtitles']['en-us']) == 1
    subtitle_url = info['subtitles']['en-us'][0]['url']

    print(f'Downloading subtitles for {id_}')
    response = requests.get(subtitle_url)
    with open(f'data/captions/raw/{id_}.xml', 'wb') as f:
        f.write(response.content)