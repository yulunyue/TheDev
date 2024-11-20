
from common.service.api import Api
import tornado
from typing import List
from tornado.httputil import HTTPServerRequest
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback, IOLoop
import _thread
import json
import signal
import sys
import json
import os
from common.util.log import logger
from common.util.module import Module
HTML_CONTENT_TYPE = dict(
    jpg="image/jpeg",
    png="image/png",
    gif="image/gif",
    css="text/css",
    html="text/html",
    svg='image/svg+xml',
    json="application/json",
    js="application/x-javascript"
)


class TornadaWebSocketConnectHandler(tornado.websocket.WebSocketHandler):
    pass


class Node:
    def __init__(self, code=0, type="", key="", title="", size=0,value=None, data=None, option=None, childs=None) -> None:
        self.code = code
        self.type = type
        self.key = key
        self.title = title
        self.value = value
        self.size = size
        self.data = data or dict()
        self.parent = None
        self.childs: List[Node] = []
        if childs:
            for cd in childs:
                if isinstance(cd,dict):
                    self.add_child(**cd)
                else:
                    self.childs.append(cd)
    def add_child(self, code=0, type="", key="", title="", value=None, data=None, option=None, childs=None):
        ret = Node(code, type, key, title,
                   value, data, option, childs=childs)
        self.childs.append(ret)
        ret.parent = self
        return ret

    def to_json(self):
        return dict(
            code=self.code,
            type=self.type,
            key=self.key,
            title=self.get_title(),
            value=self.value,
            data=self.data,
            size=self.size,
            childs=[c.to_json() for c in self.childs]
        )

    def get_title(self):
        return self.title

class ApiCall:
    def __init__(self) -> None:
        self.fun_map = dict()
        self.mock_call = []

    def add_hock(self, call):
        self.mock_call.append(call)

    def call_app(self, path, params):
        if path not in self.fun_map:
            return dict(statu=404, path=path, data=list(self.fun_map.keys()))
        ret = self.fun_map[path](**params)
        if isinstance(ret, Node):
            return ret.to_json()
        return ret

    def call(self, path, param):
        ret = self.call_app(path, param)
        for mock_fun in self.mock_call:
            mock_fun(path, param, ret)
        return ret

    def load_module_str(self, key: str, modules: List[str]):
        if key and not os.path.isdir(key):
            raise Exception(key)
        if modules == '*':
            modules = os.listdir(key)
        path_key = key if key.startswith('/') else '/'+key
        for moudule_name in modules:
            m = Module().load_module(moudule_name, key, 'Route')()
            moudule_name_key = moudule_name.replace('.', '/')
            for fun_name in dir(m):
                if fun_name.startswith('_'):
                    continue
                f = getattr(m, fun_name)
                fun_key = f'{path_key}/{moudule_name_key}/{fun_name}'
                if callable(f):
                    self.fun_map[fun_key] = f

    def load_module(self, cls):
        m = cls.Route()
        moudule_name_key = cls.__name__.replace('.', '/')
        for fun_name in dir(m):
            if fun_name.startswith('_'):
                continue
            f = getattr(m, fun_name)
            fun_key = f'/{moudule_name_key}/{fun_name}'
            if callable(f):
                self.fun_map[fun_key] = f
                logger.info(f"register {fun_key}")

    def load_modules(self, mds):
        for md in mds:
            if isinstance(md, str):
                self.load_module_str(md)
            else:
                self.load_module(md)


class MainHander(RequestHandler):
    GET_API = ApiCall()
    POST_API = ApiCall()

    def __init__(self, application: Application, request: HTTPServerRequest, **kwargs) -> None:
        self.path = request.path
        if request.method.upper() == 'POST':
            try:
                self.params = json.loads(request.body)
            except:
                self.params = {}
        else:
            self.params = request.query_arguments
        super().__init__(application, request, **kwargs)

    def get(self, *args):
        path = self.path[1:].split('?')
        ret = f'404 not find {path}'
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                ret = f.read()
        logger.info(f'{list(args)}:{len(ret)}')
        self.out(ret)

    def post(self, *args):
        ret = self.POST_API.call(self.path, self.params)
        logger.info(f'[{self.path}] [{self.params}] [{len(ret)}]')
        self.out(ret)

    def options(self, *args):
        self.out('ok')

    def out(self, data):
        self.send_header()
        self.write(data)

    def content_type(self):
        rt = HTML_CONTENT_TYPE.get(
            self.path.split(".")[-1],
            HTML_CONTENT_TYPE['json']
        )
        # print(self.path, rt)
        return rt

    def send_header(self):
        self.set_header("Content-type", self.content_type())
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")


DEFAULT_CONF_PATH = "data/setting/http.json"


def load(mds):
    config = dict(port=9999)
    if os.path.exists(DEFAULT_CONF_PATH):
        with open(DEFAULT_CONF_PATH, 'r') as f:
            config.update(json.loads(f.read()))
    MainHander.POST_API.load_modules(config.get('py_modules', [])+list(mds))
    return config


def run(*args):
    config = load(args)
    app = Application([
        (r'/ws', TornadaWebSocketConnectHandler),
        (r"/(.*)", MainHander)
    ])
    app.listen(config['port'], "0.0.0.0")
    logger.info(f"listen:{config['port']}")
    IOLoop.instance().start()


def stop():
    IOLoop.instance().stop()


def http_test(path):
    return Api().post(path)


if __name__ == "__main__":
    run(*sys.argv[1:])
