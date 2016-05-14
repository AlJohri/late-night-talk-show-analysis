import os, grequests

RAW_FOLDER = "data/raw/DXFP/"
os.makedirs(RAW_FOLDER, exist_ok=True)

FILENAME = "ds_{season:02d}{episode:03d}_act{act}.dfxp.xml"
URL = "http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_{season:02d}/episode_{episode:03d}/ds_{season:02d}{episode:03d}_act{act}.dfxp.xml"

RAW_FILEPATH = RAW_FOLDER + FILENAME

# other formats than ttml (dxfp)
# cea-608 (scc) http://a17.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/Season_21/21107/ds_21_107_act1_gfdgqnos8v.scc
# vtt http://media-resolver.mtvnservices.com/caption/convert?mgid=mgid:file:gsp:comedystor:/com/dailyshow/TDS/Season_21/21107/ds_21_107_act1_gfdgqnos8v.dfxp.xml&accountName=comedycentral.com


seasons = [16, 17, 18, 19, 20]

last_episode_per_season = {
	16: 124, # http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_16/episode_001/ds_16001_act1.dfxp.xml
    17: 157, # http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_17/episode_001/ds_17001_act1.dfxp.xml
    18: 158, # http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_18/episode_001/ds_18001_act1.dfxp.xml
    19: 159, # http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_19/episode_001/ds_19001_act1.dfxp.xml
    20: 142, # http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_20/episode_001/ds_20001_act1.dfxp.xml
}

last_episode_per_season[20] = 43 # season 20 episode 43 is last accessible with old url format (january 7 2015)

# New URL Format
# http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/Season_21/21107/ds_21_107_act1_gfdgqnos8v.dfxp.xml

def set_meta(meta):
    def hook(r, **kwargs): r.meta = meta; return r
    return hook

def handler(request, exception): print("request %s failed" % request.url)

def make_req(season, episode, act):
    return grequests.get(
        URL.format(season=season, episode=episode, act=act),
        callback=set_meta({"season": season, "episode": episode, "act": act}))

def download_reqs_to_files(reqs):
    for response in grequests.imap(reqs, exception_handler=handler):
        if response.status_code != 200:
            print("error downloading %s with code %s" % (response.url, response.status_code))
            continue
        filepath = RAW_FILEPATH.format(season=response.meta['season'], episode=response.meta['episode'], act=response.meta['act'])
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("downloaded %s" % filepath)

def subtitle_exists(season, episode, act):
    return os.path.exists(RAW_FILEPATH.format(season=season, episode=episode, act=act))

reqs = []
for season in seasons:
    for episode in range(1, last_episode_per_season[season]+1):
        for act in range(1,4+1):
            if subtitle_exists(season, episode, act): continue
            req = make_req(season, episode, act)
            reqs.append(req)

download_reqs_to_files(reqs)
