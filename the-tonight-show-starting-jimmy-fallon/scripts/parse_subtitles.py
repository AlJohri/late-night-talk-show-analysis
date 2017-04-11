#!/usr/bin/env python3

import os
from lxml import etree
from pprint import pprint as pp

raw_folder = "data/raw"
parsed_folder = "data/parsed/"
os.makedirs(parsed_folder, exist_ok=True)

for raw_filename in os.listdir(raw_folder):
    print(f'load {raw_filename}')

    raw_filepath = os.path.join(raw_folder, raw_filename)
    parsed_filepath = parsed_folder + os.path.splitext(raw_filename)[0] + ".txt"

    with open(raw_filepath) as f:
        x = f.read()
        if x == 'File not found."':
            continue

    tree = etree.parse(raw_filepath)
    root = tree.getroot()

    ns_mapping = {'ns':'http://www.w3.org/ns/ttml'}
    full_text = " ".join([ptext for ptext in root.xpath('//ns:tt/ns:body/ns:div/ns:p//text()', namespaces=ns_mapping)])

    with open(parsed_filepath, "w") as f:
        for line in full_text.split(">> "):
            line = line.strip()
            if not line: continue
            f.write(line)
            f.write("\n")

    print("write", parsed_filepath)
