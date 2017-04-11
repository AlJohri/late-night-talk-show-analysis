#!/usr/bin/env python3

import os
import json
import arrow
import requests

def download_url(url):
    print(f'Downloading: {url}')
    response = requests.get(url)
    data = response.json()
    print("found", len(data['data']), "on current page")
    print("meta total count", data['meta']['count'])
    return data

if __name__ == "__main__":
    episodes = {}
    url = "https://api.nbc.com/v3.13/videos?filter[show]=e9b05440-3d63-4eed-bc58-7de531bcd343&filter[type]=Full%20Episode&page[number]=1"
    while True:
        data = download_url(url)
        for d in data['data']:
            episodes[d['id']] = d
        if data['links'].get('next'):
            url = data['links']['next']
        else:
            break

    print('Saving episodes')
    with open('data/nbc_metadata.json', 'w') as f:
        json.dump(episodes, f)
