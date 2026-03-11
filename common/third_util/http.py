import tornado
from typing import Awaitable, List, Dict
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

from common.util.export import (
    File,
    get_log,
    uid,
    Module,
    get_function_info,
    File,
    ApiCall,
    Node,
)


logger = get_log("http")


HTML_CONTENT_TYPE = dict(
    jpg="image/jpeg",
    png="image/png",
    gif="image/gif",
    css="text/css",
    html="text/html",
    svg="image/svg+xml",
    json="application/json",
    js="application/x-javascript",
)


class TornadaWebSocketConnectHandler(WebSocketHandler):
    user_name = ""

    def open(self, *args: str, **kwargs: str):
        logger.info(f"WebSocket opened {self}")
        return super().open(*args, **kwargs)

    def hander_msg(self, node: Node):
        if node.type == "login":
            self.user_name = node.data["user_name"]
            WEB_SOCKET_CLIENTS[self.user_name] = self
            node.title = f"welcom {self.user_name}"
            return node

    def on_message(self, message):
        oj = json.loads(message)
        res = self.hander_msg(Node(type=oj["type"], data=oj["data"]))
        if res:
            self.write_message(res.to_json())

    def on_close(self):
        logger.info(f"WebSocket closed {self}")
        if self.user_name in WEB_SOCKET_CLIENTS:
            WEB_SOCKET_CLIENTS.pop(self.user_name)

    def check_origin(self, origin):
        return True


WEB_SOCKET_CLIENTS: Dict[str, TornadaWebSocketConnectHandler] = dict()


def send_clients_mag(user, data):
    WEB_SOCKET_CLIENTS[user].write_message(data)


class MainHander(RequestHandler):
    GET_API = ApiCall()
    POST_API = ApiCall()

    def __init__(
        self, application: Application, request: HTTPServerRequest, **kwargs
    ) -> None:
        self.path = request.path
        self.req_content_type: str = request.headers.get("content-type", "")
        if request.method.upper() == "POST":
            if self.req_content_type.startswith("application/json"):
                self.params = json.loads(request.body)
            else:
                self.params = dict()
        else:
            self.params = request.query_arguments
        super().__init__(application, request, **kwargs)

    def get(self, *args):
        path = self.path[1:].split("?")[0]
        ret = f"404 not find {path}"
        if os.path.isfile(path):
            with open(path, "rb") as f:
                ret = f.read()
        logger.info(f"{list(args)}:{len(ret)}")
        self.out(ret, self.params)

    def post(self, *args):
        if self.req_content_type.startswith("multipart/form-data"):
            files = dict()
            for filess in self.request.files.values():
                for f in filess:
                    files[f["filename"]] = f["body"]
            if files:
                self.params.update(files=files)
        ret = self.POST_API.call(self.path, self.params)
        logger.info(f"[{self.path}]")
        self.out(ret, self.params)

    def options(self, *args):
        self.out("ok", None)

    def out(self, data, params):
        # if params:
        #     File(f"data/log/http/{self.path}/input.json").write_file(params)
        # if data:
        #     File(f"data/log/http/{self.path}/result.json").write_file(data)
        self.send_header()
        self.write(data)

    def content_type(self):
        rt = HTML_CONTENT_TYPE.get(self.path.split(".")[-1], "")
        # print(self.path, rt)
        return rt

    def send_header(self):
        self.set_header("Content-type", self.content_type())
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")


def run(gs: Dict[str, str], port):
    MainHander.POST_API.load_modules(gs)
    app = Application(
        [(r"/ws", TornadaWebSocketConnectHandler), (r"/(.*)", MainHander)]
    )
    logger.info(f"listen:{port} pid:{os.getpid()}")
    app.listen(port, "0.0.0.0")
    IOLoop.instance().start()


def stop():
    IOLoop.instance().stop()


if __name__ == "__main__":
    run(*sys.argv[1:])
