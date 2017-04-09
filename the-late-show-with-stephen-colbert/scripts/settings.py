LATEST_EPISODE_NUMBER = 331 # http://www.imdb.com/title/tt3697842/episodes
IMDB_SERIES_ID = "tt3697842"

KINDS = ['SMPTE', 'DFXP']

RAW_FOLDER = "data/raw/{kind}/"
PARSED_FOLDER = "data/parsed/{kind}/"

FILENAME = "CBS_COLBERT_{episode:04d}_CONTENT_CIAN_caption_{kind}"

XML_FILENAME = FILENAME + ".xml"
RAW_FILEPATH = RAW_FOLDER + XML_FILENAME

URL_BASE = "http://www.cbsstatic.com/closedcaption/Current/LateNight/{kind}/"
URL = URL_BASE + XML_FILENAME
