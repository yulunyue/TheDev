import urllib.request
import urllib.parse
from http.client import HTTPResponse
import ssl

ssl_context = ssl._create_unverified_context()


def requests_get(uri, verify=False, timeout=10, headers=None, proxy=None, **kw):
    req = urllib.request.Request(uri, headers=headers or {})
    
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ssl_context))
        res: HTTPResponse = opener.open(req, timeout=timeout)
    else:
        res: HTTPResponse = urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
    
    return res.status, res.read()


def requests_post():
    pass


try:
    import requests
    import urllib3

    urllib3.disable_warnings()
except Exception as e:

    class requests:
        get = requests_get
        post = requests_post
