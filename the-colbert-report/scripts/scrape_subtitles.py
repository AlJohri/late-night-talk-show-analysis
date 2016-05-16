import os, grequests

from settings import RAW_FOLDER, XML_FILENAME, RAW_FILEPATH, URL

kind = "DFXP"
raw_folder = RAW_FOLDER.format(kind=kind)
os.makedirs(raw_folder, exist_ok=True)


seasons = [9, 9, 10, 11]

last_episode_per_season = {
    8: 155, # http://a10.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/colbert/season_08/episode_001/cr_08001_act1.dfxp.xml
    9: 155, # http://a10.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/colbert/season_09/episode_001/cr_09001_act1.dfxp.xml
    10: 161, # http://a10.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/colbert/season_10/episode_001/cr_10001_act1.dfxp.xml
    11: 39, # http://a10.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/colbert/season_11/episode_001/cr_11001_act1.dfxp.xml
}

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
        filepath = RAW_FILEPATH.format(kind=kind, season=response.meta['season'], episode=response.meta['episode'], act=response.meta['act'])
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("downloaded %s" % filepath)

def subtitle_exists(season, episode, act):
    return os.path.exists(RAW_FILEPATH.format(kind=kind, season=season, episode=episode, act=act))

reqs = []
for season in seasons:
    for episode in range(1, last_episode_per_season[season]+1):
        for act in range(1,4+1):
            if subtitle_exists(season, episode, act): continue
            req = make_req(season, episode, act)
            reqs.append(req)

download_reqs_to_files(reqs)
