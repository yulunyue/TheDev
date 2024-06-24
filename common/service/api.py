import requests
from common.util.log import log


class Api:
    CONTENT_TYPE = 'content-type'
    APPLICATION_JSON = 'application/json'

    def __init__(self, endpoint="http://127.0.0.1") -> None:
        self._endpoint = endpoint

    def get_endpoint(self):
        return self._endpoint

    def url(self, path):
        if isinstance(path, list):
            path = '/'.join(path)
        if path.startswith("http"):
            return path
        end_point = self.get_endpoint()
        if not path.startswith('/') and not end_point.endswith('/'):
            path = '/'+path
        if not end_point.startswith('http:'):
            end_point = 'https://'+end_point
        return f'{end_point}{path}'

    def get(self, url, data=None, headers=None):
        return self.http("GET", url, data=data, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.http("POST", url, data=data, headers=headers)

    def post_data(self, url, param=None, headers=None):
        return self.http("POST", url, headers=headers, param=param)

    def put(self, url, data=None, header=None):
        return self.http("PUT", url, data, header)

    def get_headers(self):
        ret = dict()
        return ret

    def get_proxy(self):
        pass

    def get_mock_data(self, key):
        pass

    def get_timeout(self):
        return 3

    def http(self, method, path, data=None, headers=None, param=None):
        if headers is None:
            headers = self.get_headers()
        uri = self.url(path)
        mock_res = self.get_mock_data(uri)
        if mock_res:
            return mock_res

        params = dict()
        if method == 'GET':
            params.update(dict(params=data))
        else:
            if param is not None:
                params.update(dict(params=param))
            if data is not None:
                params.update(dict(json=data))

        res: requests.Response = requests.request(
            url=uri,
            headers=headers,
            verify=False,
            timeout=self.get_timeout(),
            method=method,
            proxies=self.get_proxy(),
            **params
        )
        if res.status_code <= 300:
            if Api.APPLICATION_JSON in res.headers.get(Api.CONTENT_TYPE):
                return res.json()
            return res.content
        return self.hander_error(method, uri, res, data or param)

    def hander_error(self, method, uri, res: requests.Response, data):
        log.error(f'{method}:{uri}:{res.status_code}:{res.content}:{data}')

    def parse(self, value):
        return value
