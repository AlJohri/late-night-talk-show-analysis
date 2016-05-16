import os
from lxml import etree
from pprint import pprint as pp

from settings import RAW_FOLDER, PARSED_FOLDER

kind = "DFXP"
raw_folder = RAW_FOLDER.format(kind=kind)
parsed_folder = PARSED_FOLDER.format(kind=kind)
os.makedirs(parsed_folder, exist_ok=True)

for raw_filename in os.listdir(raw_folder):

    raw_filepath = raw_folder + raw_filename
    parsed_filepath = parsed_folder + raw_filename[:-4] + ".txt"
   
    try:
        tree = etree.parse(raw_filepath)
    except Exception as e:
        print("error parsing", str(e))
    root = tree.getroot()

    ns_mapping = {'ns':'http://www.w3.org/2006/10/ttaf1'}
    full_text = " ".join([ptext for ptext in root.xpath('//ns:tt/ns:body/ns:div/ns:p//text()', namespaces=ns_mapping)])

    with open(parsed_filepath, "w") as f:
        for line in full_text.split(">> "):
            line = line.strip()
            if not line: continue
            f.write(line)
            f.write("\n")

    print("write", parsed_filepath)
