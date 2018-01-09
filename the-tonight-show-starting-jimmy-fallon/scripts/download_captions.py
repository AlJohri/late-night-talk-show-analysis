#!/usr/bin/env python3

import os
import json
import requests

with open('data/caption_urls.json') as f:
    caption_urls = json.load(f)

for id_, url in caption_urls.items():
    if os.path.isfile(f'data/raw/{id_}.tt'):
        print('Already exists', f'data/raw/{id_}.tt')
    else:
        print(f'Downloading {id_} {url}')
        response = requests.get(url)
        with open(f'data/raw/{id_}.tt', 'wb') as f:
            f.write(response.content)
