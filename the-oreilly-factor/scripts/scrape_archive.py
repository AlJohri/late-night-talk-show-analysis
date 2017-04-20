#!/usr/bin/env python3

import json
import requests

with open('data/archive/archive_list.json') as f:
    archive_list = json.load(f)

for item in archive_list:
    print('Downloading', item)
    id_ = str(item['id']).zfill(4)
    html = requests.get(item['url']).content
    with open(f'data/archive/raw/{id_}.html', 'wb') as f:
        f.write(html)