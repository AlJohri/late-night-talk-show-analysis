#!/usr/bin/env python3

import feedparser
import json

entries = []

page = 1
while True:
    print(f"Page {page}")
    url = "http://tvbythenumbers.zap2it.com/tag/late-show-with-stephen-colbert-ratings/feed/?paged=" + str(page)
    d = feedparser.parse(url)
    if len(d['entries']) == 0: break
    for x in d['entries']:
        entries.append(x)
        print(x['title'])
    page += 1

with open('data/entries.json', 'w') as f:
    json.dump(entries, f, indent=4)
