import tornado
from typing import Awaitable, List, Dict
from tornado.httputil import HTTPServerRequest
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback, IOLoop
import asyncio

from common.util.export import (
    File,
    get_log,
    _thread,
    json,
    uid,
    Module,
    get_function_info,
    File,
    ApiCall,
    Node,
    signal,
    sys,
    C,
    os,
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

MAIN_IOLOOP = IOLoop.current()


class TornadaWebSocketConnectHandler(WebSocketHandler):
    hander_msg = None
    username: str = ""

    def open(self, *args: str, **kwargs: str):
        logger.info(f"WebSocket opened {self} {self.ws_connection}")
        return super().open(*args, **kwargs)

    def on_message(self, message):
        msg = Node(**json.loads(message))

        if msg.type == C.METHOD_LOGIN:
            self.username = msg.value
            self.write_message(dict(type=C.METHOD_LOGIN_OK))
        elif not self.username:
            # logger.info(f"{self.request} {message}")
            self.write_message(dict(type=C.METHOD_LOGIN))
        if TornadaWebSocketConnectHandler.hander_msg:
            TornadaWebSocketConnectHandler.hander_msg(self, msg)

    def on_close(self):
        logger.info(f"WebSocket closed {self}")
        TornadaWebSocketConnectHandler.hander_msg(
            self, Node(type=C.METHOD_LOGIN, value=self.username)
        )

    def check_origin(self, origin):
        return True

    def send_message(self, data):
        # logger.info(f"send_message {self.username} {data}")
        MAIN_IOLOOP.add_callback(self._safe_write_message, data)

    def _safe_write_message(self, data):
        if self.ws_connection and not self.ws_connection.is_closing():
            try:
                # logger.info(f"write_msg {self.username} {data}")
                self.write_message(data)
            except Exception as e:
                logger.info(f"Failed to write message: {e}")
        else:
            logger.map(user_name=self.username, c=self.ws_connection, data=data)
            TornadaWebSocketConnectHandler.hander_msg(
                self, Node(type=C.METHOD_LOGIN_OUT)
            )

    def send_data(self, data):
        self.send_message(data)


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
        self.envs = dict()
        self.envs[C.THE_DEV_USER] = request.headers.get(C.THE_DEV_USER)
        if request.method.upper() == "POST":
            if self.req_content_type.startswith("application/json"):
                self.params = json.loads(request.body)
            else:
                self.params = dict()
        else:
            self.params = request.query_arguments

        super().__init__(application, request, **kwargs)

    async def get(self, *args):
        path = self.path[1:].split("?")[0]
        ret = f"404 not find {path}"
        if os.path.isfile(path):
            with open(path, "rb") as f:
                ret = f.read()
        logger.info(f"{list(args)}:{len(ret)}")
        self.out(ret, self.params)

    async def post(self, *args):
        if self.req_content_type.startswith("multipart/form-data"):
            files = dict()
            for filess in self.request.files.values():
                for f in filess:
                    files[f["filename"]] = f["body"]
            if files:
                self.params.update(files=files)
        ret = self.POST_API.call(self.path, self.params, self.envs)
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
    MAIN_IOLOOP.start()


def stop():
    MAIN_IOLOOP.stop()


if __name__ == "__main__":
    run(*sys.argv[1:])
