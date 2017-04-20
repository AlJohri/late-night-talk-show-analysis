#!/usr/bin/env python3

import os
import json
import lxml.html

for filename in reversed(os.listdir('data/archive/raw/')):
    print(filename)
    with open(f'data/archive/raw/{filename}') as f:
        html = f.read()
    doc = lxml.html.fromstring(html)
    video_ids = [
        int(link.get('src').replace('//video.foxnews.com/v/embed.js?id=', '').replace('&w=466&h=263', ''))
        for link in doc.cssselect("script[src^='//video.foxnews.com']")
    ]

    output = {
        'video_ids': video_ids
    }

    print(output)

    new_filename = filename.replace('.html', '.json')
    with open(f'data/archive/parsed/{new_filename}', 'w') as f:
        json.dump(output, f)