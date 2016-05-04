import os, grequests

os.makedirs("data/", exist_ok=True)

LATEST_EPISODE_NUMBER = 134 # May 3 2016 - http://www.imdb.com/title/tt3697842/episodes

filename = "CBS_COLBERT_{episode:04d}_CONTENT_CIAN_caption_{kind}.xml"
filepath = "data/" + filename
url = "http://www.cbsstatic.com/closedcaption/Current/LateNight/{kind}/" + filename

def handler(request, exception):
    print("request %s failed" % request.url)
    import pdb; pdb.set_trace()

def make_req(kind, i): return grequests.get(url.format(kind=kind, episode=i))
def exists(kind, i): return os.path.exists(filepath.format(kind=kind, episode=i))

def download_reqs_to_files(reqs):
    for response in grequests.imap(reqs, exception_handler=handler):
        if response.status_code != 200:
            print("error downloading %s with code %s" % (response.url, response.status_code))
            continue
        filename = response.url.split("/")[-1]
        with open("data/" + filename, "wb") as f:
            f.write(response.content)
        print("downloaded %s" % filename)

reqs = (make_req("SMPTE", i) for i in range(1, LATEST_EPISODE_NUMBER) if not exists("SMPTE", i))
download_reqs_to_files(reqs)

reqs = (make_req("DFXP", i) for i in range(1, LATEST_EPISODE_NUMBER) if not exists("DFXP", i))
download_reqs_to_files(reqs)