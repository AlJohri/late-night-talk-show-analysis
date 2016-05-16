RAW_FOLDER = "data/raw/{kind}/"
PARSED_FOLDER = "data/parsed/{kind}/"

FILENAME = "cr_{season:02d}{episode:03d}_act{act}.dfxp"
XML_FILENAME = FILENAME + ".xml"

URL = "http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/colbert/season_{season:02d}/episode_{episode:03d}/cr_{season:02d}{episode:03d}_act{act}.dfxp.xml"

RAW_FILEPATH = RAW_FOLDER + XML_FILENAME
