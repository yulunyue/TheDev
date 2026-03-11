import urllib.request
import urllib.parse
from http.client import HTTPResponse
import ssl

ssl_context = ssl._create_unverified_context()


def requests_get(uri, verify=False, timeout=10, headers=None, **kw):
    req = urllib.request.Request(uri, headers=headers)
    res: HTTPResponse = urllib.request.urlopen(
        req, timeout=timeout, context=ssl_context
    )
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
