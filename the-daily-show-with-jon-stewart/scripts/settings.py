IMDB_SERIES_ID="tt0115147" # for the daily show with jon stewart and trevor noah

RAW_FOLDER = "data/raw/{kind}/"
PARSED_FOLDER = "data/parsed/{kind}/"

FILENAME = "ds_{season:02d}{episode:03d}_act{act}.dfxp"

XML_FILENAME = FILENAME + ".xml"
RAW_FILEPATH = RAW_FOLDER + XML_FILENAME

URL = "http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_{season:02d}/episode_{episode:03d}/ds_{season:02d}{episode:03d}_act{act}.dfxp.xml"