import requests
from common.util.export import (
    get_log,
    File,
    get_cache,
    hash_any,
    ThreadManage,
    json_dumps,
)
import urllib3

urllib3.disable_warnings()
logger = get_log("api")
from common.tool.export import NumberModel, StrModel, ConfigBase, TableBase, DictModel


class ApiConfig(ConfigBase):
    endpoint = StrModel()
    cookie = DictModel()
    proxy = DictModel()
    timeout = NumberModel(default_value=10)
    user_name = StrModel()
    pass_word = StrModel()


API_CONFIG = TableBase[ApiConfig]().set_resource("api")


def get_proxy(key=None):
    ret = API_CONFIG.get("default").proxy.get_value() or dict(https=None, http=None)
    if key is None:
        return ret
    return ret[key]


def request_mock():
    import socket

    socket.setdefaulttimeout(1)

    def mock(fun, method: str):
        def wrap(url, timeout=None, proxies=None, self=None, verify=False, **kw):
            if timeout is None:
                timeout = API_CONFIG.get("default").timeout.get_value()
            if proxies is None:
                proxies = get_proxy()
            if verify:
                verify = False
            err_msg = ""
            logger.debug(f"pre {method} {url} {timeout} {proxies} {kw}")
            try:
                if self is None:
                    ret: requests.Response = fun(
                        url, timeout=timeout, proxies=proxies, verify=verify, **kw
                    )
                else:
                    ret: requests.Response = fun(
                        self, url, timeout=timeout, proxies=proxies, verify=verify, **kw
                    )
                err_msg = f"{ret.status_code}"
            except Exception as e:
                err_msg = str(e)
                raise Exception(e)
            finally:
                logger.debug(f"finish {url} {err_msg}")
            return ret

        def wrap_cls(self, url, timeout=None, proxies=None, **kw):
            return wrap(url, timeout=timeout, proxies=proxies, self=self, **kw)

        if method.startswith("s_"):
            return wrap_cls
        return wrap

    class MockSession(requests.Session):
        get = mock(requests.Session.get, "s_get")
        post = mock(requests.Session.get, "s_post")

    requests.Session = MockSession
    requests.get = mock(requests.get, "get")
    requests.post = mock(requests.post, "post")
    requests.put = mock(requests.put, "put")


class Api:
    CONTENT_TYPE = "content-type"
    APPLICATION_JSON = "application/json"

    def __init__(self, log_enable=False):
        self._name = self.__class__.__name__
        self.log_enable = log_enable
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
        return API_CONFIG.get(self.name).endpoint.get_value()

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

    def get(self, url, data=None, timeout=None, headers=None):
        return self.http(
            "GET",
            url,
            data=data,
            headers=headers,
            timeout=timeout,
        )

    def download(self, url: str, dst=None, data=None, timeout=3600):
        if dst is None:
            dst = f"/Thedev/data/download/{url.split('/').pop().split('?')[0]}"
        f = File(dst)
        # if f.exists():
        #     return f
        self.http(
            "GET", url, data, timeout=timeout, stream=True, writer=f.get_bin_writer()
        )
        return f

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
        return API_CONFIG.get(self.name).proxy.get_value()

    def get_mock_data(self, uri, method, param):
        k = method + "|" + hash_any(uri) + "|" + hash_any(param)
        if self.cache and self.cache.exists(k):
            return k, self.cache.get(k)
        return k, None

    def get_timeout(self):
        return API_CONFIG.get(self.name).timeout.get_value()

    def http(
        self,
        method,
        path,
        data=None,
        headers=None,
        param=None,
        timeout=None,
        stream=False,
        writer=None,
    ):
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
        timeout = timeout or self.get_timeout()

        params = dict()
        if method == "GET":
            if data:
                params.update(dict(params=data))
            if stream:
                params.update(dict(stream=True))
        else:
            if param is not None:
                params.update(dict(params=param))
            if data is not None:
                params.update(dict(json=data))
        cookies = API_CONFIG.get(self.name).cookie.get_value() or {}
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
        if stream:
            res.raise_for_status()
            from common.third_util.tqdm_util import tqdm

            total = int(res.headers.get("content-length", 0))
            t = tqdm(total=total, unit="iB", unit_scale=True)
            for data in res.iter_content(chunk_size=8192):
                writer.write(data)
                t.update(len(data))
            t.close()
            return
        if res.status_code <= 300:
            content_type = res.headers.get(Api.CONTENT_TYPE)
            ret = res.content
            if Api.APPLICATION_JSON in content_type:
                ret = res.json()
                if self.log_enable:
                    logger.debug(
                        f"DO HTTP [{method}] {uri} {proxies} {timeout} length={len(ret)}\n {json_dumps(ret)[:100]} "
                    )
            else:
                logger.debug(content_type)
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
