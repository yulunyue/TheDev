
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
from importlib import import_module
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


class ApiCall:
    def __init__(self) -> None:
        self.fun_map = dict()

    def call(self, path, params):
        if path not in self.fun_map:
            return dict(statu=404, path=path, data=list(self.fun_map.keys()))
        return self.fun_map[path](**params)

    def load_module(self, key: str, modules: List[str]):
        if key and not os.path.isdir(key):
            raise Exception(key)
        if key not in sys.path:
            sys.path += [key]
        if modules == '*':
            modules = os.listdir(key)
        path_key = key if key.startswith('/') else '/'+key
        for moudule_name in modules:
            m = getattr(import_module(moudule_name), 'Route')()
            moudule_name_key = moudule_name.replace('.', '/')
            for fun_name in dir(m):
                if fun_name.startswith('_'):
                    continue
                f = getattr(m, fun_name)
                fun_key = f'{path_key}/{moudule_name_key}/{fun_name}'
                if callable(f):
                    self.fun_map[fun_key] = f

    def load_modules(self, data: dict):
        for key, value in data.items():
            self.load_module(key, value)


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
        self.out(ret)

    def post(self, *args):
        self.out(self.POST_API.call(self.path, self.params))

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


def run(path: str = DEFAULT_CONF_PATH):
    config = dict()
    with open(path, 'r') as f:
        config.update(json.loads(f.read()))
    if 'py_modules' in config:
        MainHander.POST_API.load_modules(config['py_modules'])

    app = Application([
        (r'/ws', TornadaWebSocketConnectHandler),
        (r"/(.*)", MainHander)
    ])
    app.listen(config['port'])
    IOLoop.instance().start()


def start(f):
    def util():
        f()
    c = PeriodicCallback(util, 1)
    c.start()
    run()


def stop():
    IOLoop.instance().stop()
    exit()


if __name__ == "__main__":
    run(*sys.argv[1:])
