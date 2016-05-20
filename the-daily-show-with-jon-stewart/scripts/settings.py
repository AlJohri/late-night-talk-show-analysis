IMDB_SERIES_ID="tt0115147" # for the daily show with jon stewart and trevor noah
COMEDY_CENTRAL_SERIES_ID="2796e828-ecfd-11e0-aca6-0026b9414f30"

RAW_FOLDER = "data/raw/{kind}/"
PARSED_FOLDER = "data/parsed/{kind}/"

FILENAME = "ds_{season:02d}{episode:03d}_act{act}.dfxp"

XML_FILENAME = FILENAME + ".xml"
RAW_FILEPATH = RAW_FOLDER + XML_FILENAME

URL = "http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_{season:02d}/episode_{episode:03d}/ds_{season:02d}{episode:03d}_act{act}.dfxp.xml"