import requests
from common.util.export import (
    get_log,
    File,
    get_cache,
    hash_any,
    SingletonUtil,
    ThreadManage,
)
from common.tool.export import NumberModel, StrModel, ConfigBase, TableBase, DictModel
import urllib3

urllib3.disable_warnings()
logger = get_log("api")


class ApiConfig(ConfigBase):
    endpoint = StrModel()
    cookie = DictModel()
    proxy = DictModel()
    timeout = NumberModel(default_value=10)


class Api:
    CONTENT_TYPE = "content-type"
    APPLICATION_JSON = "application/json;charset=UTF-8"

    def __init__(self):
        self._name = self.__class__.__name__
        self.c = TableBase[ApiConfig]().set_resource("api")
        self.cache = None

    @property
    def name(self):
        return self._name

    def set_cache(self, cache=None):
        if cache is None:
            self.cache = get_cache(
                self.get_endpoint().replace(":", "_").replace("/", "_")
            )
        else:
            self.cache = cache
        return self

    def get_endpoint(self):
        return self.endpoint.get_value()

    def url(self, path):
        if isinstance(path, list):
            path = "/".join(path)
        if path.startswith("http"):
            return path
        end_point = self.get_endpoint()
        if not path.startswith("/") and not end_point.endswith("/"):
            path = "/" + path
        if not end_point.startswith("http"):
            end_point = "https://" + end_point
        return f"{end_point}{path}"

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
        return self.c.get(self.name).proxy.get_value()

    def get_mock_data(self, uri, method, param):
        k = method + "|" + hash_any(uri) + "|" + hash_any(param)
        if self.cache and self.cache.exists(k):
            return k, self.cache.get(k)
        return k, None

    def get_timeout(self):
        return self.c.get(self.name).timeout.get_value()

    def http(self, method, path, data=None, headers=None, param=None):
        if headers is None:
            headers = self.get_headers()
        headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            }
        )
        uri = self.url(path)
        key, mock_res = self.get_mock_data(path, method, data or param)
        if mock_res:
            return mock_res
        proxies = self.get_proxy()
        timeout = self.get_timeout()
        logger.info(f"DO HTTP [{method}] {uri} {proxies} {timeout}")
        params = dict()
        if method == "GET":
            params.update(dict(params=data))
        else:
            if param is not None:
                params.update(dict(params=param))
            if data is not None:
                params.update(dict(json=data))
        cookies = self.c.get(self.name).cookie.get_value() or {}
        res: requests.Response = requests.request(
            url=uri,
            headers=headers,
            verify=False,
            cookies=cookies,
            timeout=timeout,
            method=method,
            proxies=proxies,
            **params,
        )
        if res.status_code <= 300:
            content_type = res.headers.get(Api.CONTENT_TYPE)
            ret = res.content
            if content_type in Api.APPLICATION_JSON:
                ret = res.json()
            else:
                logger.info(content_type)
            if self.cache:
                self.cache.set(key, ret)
            return ret
        return self.hander_error(method, uri, res, data or param, cookies)

    def hander_error(self, method, uri, res: requests.Response, data, cookies):
        File("data/log/http/http_error.html").write_file(res.content)
        raise Exception(
            f"{method}:{uri}:{res.status_code}:{res.content[:256]}:{str(data)[:40]},{cookies}"
        )

    def parse(self, value):
        return value

    _ins = None

    @classmethod
    def ins(cls):
        if cls._ins is None:
            cls._ins = cls().set_cache()
        return cls._ins
