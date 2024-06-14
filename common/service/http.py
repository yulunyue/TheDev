
import tornado
from tornado.httputil import HTTPServerRequest
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback, IOLoop
import signal
import sys
import json
import os
HTML_CONTENT_TYPE = dict(
    jpg="image/jpeg",
    png="image/png",
    gif="image/gif",
    css="text/css",
    html="text/html",
    svg='image/svg+xml',
    js="application/x-javascript"
)

class TornadaWebSocketConnectHandler(tornado.websocket.WebSocketHandler):
    pass


class MainHander(RequestHandler):
    def __init__(self, application: Application, request: HTTPServerRequest, **kwargs) -> None:
        self.path = request.path
        if request.method.upper() == 'POST':
            try:
                self.params = json.loads(request.body)
            except:
                self.params={}
        else:
            self.params = request.query_arguments
        super().__init__(application, request, **kwargs)

    def get(self, *args):
        ways = self.path.split('/')[1:]
        if hasattr(UTIL,ways[0]):
            try:
                data=getattr(UTIL,ways[0])(*ways[1:])
            except Exception as e:
                import traceback
                data=traceback.format_exc()
            if isinstance(data,str):
                self.out(f'<pre>{data}</pre>')
            else:
                self.out(data)
            return 
        path = f'hcso_tool/vt/font{self.path}'
        ret = f'404 not find {path}'
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                ret = f.read()
        self.out(ret)

    def post(self, *args):
        self.out(Url.call(self.path, self.params))

    def options(self, *args):
        self.out('ok')

    def out(self, data):
        self.send_header()
        self.write(data)

    def content_type(self):
        rt = HTML_CONTENT_TYPE.get(self.path.split(".")[-1], "text/html")
        # print(self.path, rt)
        return rt

    def send_header(self):
        self.set_header("Content-type", self.content_type())
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")



def run():
    port = 9000
    app = Application([
        (r'/ws', TornadaWebSocketConnectHandler),
        (r"/(.*)", MainHander)
    ])
    # signal.signal(signal.SIGINT, MainHander.stop)
    app.listen(port)
    IOLoop.instance().start()



    