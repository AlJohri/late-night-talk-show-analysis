#!/usr/bin/env python3

import re
import json
import arrow
import lxml.html
import requests

with open('data/transcript_list.json') as f:
    transcript_list_gen = (json.loads(line) for line in f)
    transcript_list = sorted(transcript_list_gen, key=lambda x: x['date'])

def find_article_id(doc):
    scripts = doc.cssselect("script")
    script = [script for script in scripts if "var articleInfo" in script.text_content()][0].text_content()
    vcmId = re.search(r"vcmId: \"(.*)\"", script).groups()[0]
    return vcmId

def find_transcript_element(doc):
    article = doc.cssselect("div.main > article > div > div.article-body > div.article-text")[0]
    return article

def download_article(url):
    response = requests.get(url)
    doc = lxml.html.fromstring(response.content)
    vcmId = find_article_id(doc)
    transcript_el = find_transcript_element(doc)
    return {
        "vcmId": vcmId,
        "html": lxml.html.tostring(transcript_el).decode('utf-8')
    }

with open('data/transcript_list_ids.json', 'w') as f:
    pass

for item in transcript_list:
    url = item.pop('url')[0]

    print(f"Downloading {url}")
    article = download_article(url)
    vcmId, html = article['vcmId'], article['html']

    output = {
        "vcmId": vcmId,
        "url": url,
        "html": html,
        "title": item['title'],
        "description": item['description'],
        "date": item['date']
    }

    with open(f'data/raw/{vcmId}.json', 'w') as f:
        json.dump(output, f)
