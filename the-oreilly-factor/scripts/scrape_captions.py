#!/usr/bin/env python3

import os
import json
import requests
from youtube_dl import YoutubeDL

from blessings import Terminal
t = Terminal()

print("Loading video segment ids...")

video_ids = set()
for filename in os.listdir('data/archive/parsed/'):
    with open(f'data/archive/parsed/{filename}') as f:
        video_ids |= set(json.load(f)['video_ids'])

print(f"Loaded {len(video_ids)} video segment ids...")

yd = YoutubeDL()

for i, id_ in enumerate(video_ids):

    metadata_filename = f'data/metadata/parsed/{id_}.json'
    if os.path.isfile(metadata_filename):
        print(f'[{i}] Already downloaded metadata for {id_}')
        with open(metadata_filename) as f:
            info = json.load(f)
    else:
        print(f'[{i}] Downloading metadata for {id_}')
        url = f'http://video.foxnews.com/v/{id_}/'
        try:
            info = yd.extract_info(url, download=False, ie_key='FoxNews', process=False)
        except Exception as e:
            print(e)
            print(t.red(f"Ran into an error while trying to download metadata for {id_}"))
            continue
        with open(metadata_filename, 'w') as f:
            json.dump(info, f, indent=4)

    subtitle_filename = f'data/captions/raw/{id_}.xml'
    if os.path.isfile(subtitle_filename):
        print(f'[{i}] Already downloaded subtitles for {id_}')
    else:
        try:
            subtitle_url = info['subtitles']['en-us'][0]['url']
        except KeyError:
            print(t.yellow(f'No subtitles found for {id_}'))
            continue

        print(f'[{i}] Downloading subtitles for {id_}')
        assert len(info['subtitles']['en-us']) == 1
        response = requests.get(subtitle_url)
        with open(subtitle_filename, 'wb') as f:
            f.write(response.content)
