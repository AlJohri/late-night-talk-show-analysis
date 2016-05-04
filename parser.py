from lxml import etree
from pprint import pprint as pp

filename = "CBS_COLBERT_{episode:04d}_CONTENT_CIAN_caption_{kind}.xml"
filepath = "data/" + filename

for i in range(1, 20):
    path = filepath.format(kind="DFXP", episode=i)

    tree = etree.parse(path)
    root = tree.getroot()

    ns_mapping = {'ns':'http://www.w3.org/ns/ttml'}
    full_text = " ".join([ptext for ptext in root.xpath('//ns:tt/ns:body/ns:div/ns:p//text()', namespaces=ns_mapping)])

    pp(full_text.split(">>"))