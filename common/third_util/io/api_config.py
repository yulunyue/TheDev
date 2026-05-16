from .http_util import requests
from common.util.export import get_dev_log, File
from common.tool.export import NumberModel, StrModel, FileConfig, DictModel

logger = get_dev_log("api")

USER_AGENT_DEFAULT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"


class ApiConfig(FileConfig):
    endpoint = StrModel()
    cookie = DictModel()
    proxy = DictModel()
    headers = DictModel()
    timeout = NumberModel(default_value=10)
    user_name = StrModel()
    pass_word = StrModel()
    config = DictModel()


API_CONFIG = ApiConfig.set_resource("config/setting/api.json")


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
