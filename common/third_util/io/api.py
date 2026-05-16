from .http_util import requests
from common.util.export import get_dev_log, File, get_cache, hash_any_str, json_dumps
from .api_config import API_CONFIG, USER_AGENT_DEFAULT

logger = get_dev_log("api")


class Api:
    CONTENT_TYPE = "content-type"
    APPLICATION_JSON = "application/json"
    LOG_ENABLE_DEFAULT = False

    def __init__(self, name="", log_enable=False):
        self._name = name or self.__class__.__name__
        self.log_enable = log_enable or self.__class__.LOG_ENABLE_DEFAULT
        self.cache = None

    @classmethod
    def enable_globel_log(cls):
        cls.LOG_ENABLE_DEFAULT = True

    @property
    def name(self):
        return self._name

    def get_config(self, name, default_value=None):
        return API_CONFIG.get(self.name).config.get(name, default_value)

    def set_cache(self, cache=None):
        if cache is None:
            self.cache = get_cache(
                self.get_endpoint().replace(":", "_").replace("/", "_")
            )
        else:
            self.cache = cache
        return self

    end_point = ""

    def get_endpoint(self):
        if self.end_point:
            return self.end_point
        return API_CONFIG.get(self.name).endpoint.get_value()

    def get_password(self):
        return API_CONFIG.get(self.name).pass_word.get_value()

    def get_username(self):
        return API_CONFIG.get(self.name).user_name.get_value()

    def set_endpoint(self, s):
        self.end_point = s
        return self

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
        f = File(dst).make_dir_if_not_exist()
        if f.exists():
            return f
        self.http(
            "GET", url, data, timeout=timeout, stream=True, writer=f.get_bin_writer()
        )
        return f

    def post(self, url, data=None, headers=None, cookies=None):
        return self.http("POST", url, data=data, headers=headers, cookies=cookies)[1]

    def post_res(self, url, data=None, headers=None):
        return self.http("POST", url, data=data, headers=headers)[0]

    def post_data(self, url, param=None, headers=None):
        return self.http("POST", url, headers=headers, param=param)[1]

    def post_files(self, url, path, name="file"):
        return self.http(
            "POST",
            url,
            files={name: open(path, "rb")},
        )

    def put(self, url, data=None, header=None):
        return self.http("PUT", url, data, header)

    def get_headers(self):
        return API_CONFIG.get(self.name).headers.get_value()

    def get_proxy(self):
        return API_CONFIG.get(self.name).proxy.get_value()

    def get_mock_data(self, uri, method, param):
        k = method + "|" + hash_any_str(uri) + "|" + hash_any_str(param)
        if self.cache and self.cache.exists(k):
            return k, self.cache.get(k)
        return k, None

    def get_timeout(self):
        return API_CONFIG.get(self.name).timeout.get_value()

    def log(
        self,
        uri,
        res: requests.Response,
        method,
        params,
        headers,
        cookies,
        content,
        proxies,
    ):
        if not self.log_enable:
            return
        logger.info(
            f"---begin uri:{uri} res_url:{res.url} method:{method} status:{res.status_code}---"
        )
        if params:
            logger.info(f"req_body:{json_dumps(params,indent=2)}")
        if proxies:
            logger.info(f"proxies: {proxies}")
        if headers:
            logger.info(f"req_headers: {json_dumps(dict(headers),indent=2)}")
        if cookies:
            logger.info(f"req_cookies: {json_dumps(dict(cookies),indent=2)}")
        if isinstance(content, bytes):
            logger.info(f"res_body: {content}")
        else:
            logger.info(f"res_body: {json_dumps(content,indent=2)}")
        logger.info(f"res_headers: {json_dumps(dict(res.headers.copy()),indent=2)}")
        logger.info(f"res_cookies: {json_dumps(dict(res.cookies.copy()),indent=2)}")
        logger.info(f"---end---")

    def http(
        self,
        method,
        path,
        data=None,
        headers=None,
        cookies: dict = None,
        files=None,
        param=None,
        timeout=None,
        stream=None,
    ):
        if headers is None:
            headers = self.get_headers()
        if "User-Agent" not in headers:
            headers["User-Agent"] = USER_AGENT_DEFAULT
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
            if files is not None:
                params.update(files=files)
            if param is not None:
                params.update(dict(params=param))
            if data is not None:
                params.update(dict(json=data))

        if cookies is None:
            cookies = API_CONFIG.get(self.name).cookie.get_value()
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
        content_type = res.headers.get(Api.CONTENT_TYPE, "")
        if Api.APPLICATION_JSON in content_type:
            try:
                ret = res.json()
            except Exception as e:
                ret = res.content
        else:
            ret = res.content
        if res.status_code > 300:
            raise Exception(res.status_code, res.url, res.text[:128])
        self.log(uri, res, method, data or param, headers, cookies, ret, proxies)
        return res, ret

    def hander_stream(self, res: requests.Response, stream=False, writer=None):
        res.raise_for_status()
        from common.third_util.tqdm_util import tqdm

        total = int(res.headers.get("content-length", 0))
        t = tqdm(total=total, unit="iB", unit_scale=True)
        for data in res.iter_content(chunk_size=8192):
            writer.write(data)
            t.update(len(data))
        t.close()
        return

    def parse(self, value):
        return value
