def set_meta(meta):
    def hook(r, **kwargs): r.meta = meta; return r
    return hook
def handler(request, exception): print("request %s failed" % request.url)