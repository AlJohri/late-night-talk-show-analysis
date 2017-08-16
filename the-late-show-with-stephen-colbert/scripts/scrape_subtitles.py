#!/usr/bin/env python3

import sys; sys.path.append("../lib/")
import os, grequests

EPISODES_TO_SKIP = [38, 39, 40, 52]

from settings import KINDS, URL, RAW_FOLDER, RAW_FILEPATH, LATEST_EPISODE_NUMBER
from utils import set_meta, handler

def make_req(kind, i):
    return grequests.get(URL.format(kind=kind, episode=i), callback=set_meta({"kind": kind, "i": i}))

def subtitle_exists(kind, i):
    return os.path.exists(RAW_FILEPATH.format(kind=kind, episode=i))

def download_reqs_to_files(reqs):
    for response in grequests.imap(reqs, exception_handler=handler):
        if response.status_code != 200:
            print("error downloading %s with code %s" % (response.url, response.status_code))
            continue
        filepath = RAW_FILEPATH.format(kind=response.meta['kind'], episode=response.meta['i'])
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("downloaded %s" % filepath)

for kind in KINDS:
    raw_folder = RAW_FOLDER.format(kind=kind)
    os.makedirs(raw_folder, exist_ok=True)
    reqs = (make_req(kind, i) for i in range(1, LATEST_EPISODE_NUMBER+1) if not subtitle_exists(kind, i) and i not in EPISODES_TO_SKIP)
    download_reqs_to_files(reqs)
