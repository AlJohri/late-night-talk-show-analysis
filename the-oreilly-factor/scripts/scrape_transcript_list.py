#!/usr/bin/env python3

import requests, json, logging, time
from functools import partial
from urllib.parse import urlencode, quote

custom_urlencode = partial(urlencode, quote_via=quote)
custom_urlencode.__doc__ = """
FOX's solr api wrapper requires "%20" instead of "+" for spaces.
The default `urllib.parse.quote_plus` will use "+" signs for spaces.
`urllib.parse.quote` does not.
"""

logging.basicConfig(level='DEBUG')

def strip_jsonp_callback(function_name, text):
    prefix = function_name + "("
    suffix = ")"
    if text.startswith(prefix) and text.endswith(suffix):
        return text[len(prefix):-len(suffix)]
    else:
        print(prefix, suffix, text)
        raise ValueError("invalid jsonp")

def get_jsonp(url, **kwargs):
    params = kwargs.pop('params')
    full_url = url + '?' + custom_urlencode(params)
    logging.debug(f"Requesting: {full_url}")
    response = requests.get(full_url, **kwargs)
    response.raise_for_status()
    if response.status_code == 301:
        raise Exception(f"FOX attempted to redirect. This means "
                        f"the request failed. Request URL was: {full_url}")
    raw_json = strip_jsonp_callback(params['callback'], response.text)
    return json.loads(raw_json)

def get_stories(start=0):

    params = {
        "q": "",
        "taxonomy.path": "/FOX NEWS/SHOWS/Oreilly Factor",
        "date": "[* TO *]",
        "start": start,
        "sort": "latest",
        "callback": "callback"
    }

    while True:
        data = get_jsonp("http://api.foxnews.com/v0.1/search/", params=params, allow_redirects=False)
        docs = data['response'].pop('docs')
        logging.debug(f"current page: {str(data['response'])}")
        yield from docs
        params['start'] += len(docs)
        # Fox has a hard limit as "990" as the last offset and it must be in multiples of 10
        if params['start'] >= 1000:
            break
        time.sleep(5)

if __name__ == "__main__":

    # start downloading
    # ./scripts/scrape_transcript_list.py

    # continue downloading
    # ./scripts/scrape_transcript_list.py --keep --start 920

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--keep', action='store_true', default=False)
    parser.add_argument('--start', type=int, default=0)
    args = parser.parse_args()

    if not args.keep:
        with open('data/stories.json', 'w') as f:
            pass

    story_iterator = get_stories(args.start)
    for i, story in enumerate(story_iterator):
        date, title = story['date'], story['title']
        print(i, date, title)
        with open('data/stories.json', 'a') as f:
            f.write(json.dumps(story) + "\n")
