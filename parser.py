import os
from lxml import etree
from pprint import pprint as pp

from settings import KINDS, URL, RAW_FOLDER, PARSED_FOLDER

kind = "DFXP"

raw_folder = RAW_FOLDER.format(kind=kind)
parsed_folder = PARSED_FOLDER.format(kind=kind)
os.makedirs(parsed_folder, exist_ok=True)

for raw_filename in os.listdir(raw_folder):

    raw_filepath = raw_folder + raw_filename

    tree = etree.parse(raw_filepath)
    root = tree.getroot()

    ns_mapping = {'ns':'http://www.w3.org/ns/ttml'}
    full_text = " ".join([ptext for ptext in root.xpath('//ns:tt/ns:body/ns:div/ns:p//text()', namespaces=ns_mapping)])
    # pp(full_text.split(">>"))

    parsed_filepath = parsed_folder + raw_filename[:-4] + ".txt"

    with open(parsed_filepath, "w") as f:
        f.write(full_text)

    print("write", parsed_filepath)