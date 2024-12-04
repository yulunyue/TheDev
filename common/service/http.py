
from common.service.api import Api
import tornado
from typing import Awaitable, List,Dict
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
from common.util.tool import uid
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

class Node:
    def __init__(self, code=0,  direction=-1,type="", key="", title="", size=0,value=None, data=None, option=None, childs=None) -> None:
        self.code = code
        self.type = type
        self.key = key or uid('node')
        self.title = title
        self.value = value
        self.size = size
        self.data = data or dict()
        self.parent = None
        self.childs: List[Node] = []
        self.direction = direction
        if childs:
            for cd in childs:
                if isinstance(cd,dict):
                    self.add_child(**cd)
                else:
                    self.childs.append(cd)
        self.init()
    def init(self):
        pass
    def set_type(self,tp):
        self.type=tp
        return self
    
    def set_key(self,key):
        self.key=key
        return self
    
    def set_data(self,**kw):
        for k,v in kw.items():
            self.data[k]=v
        return self

    def set_option(self,**kwargs):
        pass

    def add_child(self, code=0, type="", key="", title="", value=None, data=None, option=None, childs=None):
        ret = Node(code=code, type=type, key=key, title=title,
                   value=value, data=data, option=option, childs=childs)
        self.childs.append(ret)
        ret.parent = self
        return ret

    def to_json(self):
        return dict(
            type=self.type,
            key=self.key,
            title=self.get_title(),
            value=self.value,
            childs=[c.to_json() for c in self.childs]
        )

    def get_title(self):
        return self.title
    
    def get_data(self):
        return self.data
    
class TornadaWebSocketConnectHandler(WebSocketHandler):
    user_name=""
    def open(self, *args: str, **kwargs: str) -> Awaitable[None] | None:
        logger.info(f"WebSocket opened {self}")
        return super().open(*args, **kwargs)
    
    def hander_msg(self,node:Node):
        if node.type == 'login':
            self.user_name=node.data['user_name']
            WEB_SOCKET_CLIENTS[self.user_name]=self
            node.title = f'welcom {self.user_name}'
            return node
        
    def on_message(self, message):
        oj = json.loads(message)
        res = self.hander_msg(Node(type=oj['type'],data=oj['data']))
        if res:
            self.write_message(res.to_json())

    def on_close(self):
        logger.info(f"WebSocket closed {self}")
        if self.user_name in WEB_SOCKET_CLIENTS:
            WEB_SOCKET_CLIENTS.pop(self.user_name)
        
    def check_origin(self, origin):
        return True


WEB_SOCKET_CLIENTS:Dict[str,TornadaWebSocketConnectHandler] = dict()

def send_clients_mag(user, data):
    WEB_SOCKET_CLIENTS[user].write_message(data)
 

class ApiCall:
    def __init__(self) -> None:
        self.fun_map = dict()
        self.mock_call = []

    def add_hock(self, call):
        self.mock_call.append(call)

    def call_app(self, path, params):
        if path not in self.fun_map:
            return dict(statu=404, path=path, data=list(self.fun_map.keys()))
        try:
            ret = self.fun_map[path](**params)
        except Exception as e:
            logger.error(e)
            import traceback
            traceback.print_exc()
            ret = dict(code=500,title=str(e))
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
        path = self.path[1:].split('?')[0]
        ret = f'404 not find {path}'
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                ret = f.read()
        logger.info(f'{list(args)}:{len(ret)}')
        self.out(ret)

    def post(self, *args):
        ret = self.POST_API.call(self.path, self.params)
        logger.info(f'[{self.path}]')
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





def run(*args,port=8888):
    MainHander.POST_API.load_modules(list(args))
    app = Application([
        (r'/ws', TornadaWebSocketConnectHandler),
        (r"/(.*)", MainHander)
    ])
    logger.info(f"listen:{port}")
    app.listen(port, "0.0.0.0")
    IOLoop.instance().start()


def stop():
    IOLoop.instance().stop()


def http_test(path):
    return Api().post(path)


if __name__ == "__main__":
    run(*sys.argv[1:])
