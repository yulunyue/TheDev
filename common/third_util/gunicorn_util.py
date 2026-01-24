import sys
from gunicorn.app.wsgiapp import WSGIApplication
import threading
import time
from common.tool.export import OsUtil


class GunicornApp(WSGIApplication):
    def __init__(self, app, options=None):
        self.app = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        # 加载配置
        if self.options:
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key, value)

    def load(self):
        return self.app


def app(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "application/json")]
    start_response(status, headers)
    return [b"Hello, World!"]


class GunicornUtil:
    def get_options(self):
        return {
            "bind": "0.0.0.0:8090",
            "workers": 4,
            "worker_class": "sync",
            "threads": 2,
            "timeout": 30,
            "keepalive": 2,
            "accesslog": "-",  # 输出到标准输出
            "errorlog": "-",  # 输出到标准错误
            "loglevel": "debug",
            "preload_app": False,
            "reload": False,  # 开发时设为 True 可自动重载
            "worker_connections": 1000,
            "max_requests": 1000,
            "max_requests_jitter": 50,
            "graceful_timeout": 30,
            "limit_request_line": 4094,
            "limit_request_fields": 100,
            "limit_request_field_size": 8190,
        }

    def run(self):
        self.gunicorn_app = GunicornApp(app, self.get_options())
        self.gunicorn_app.run()

    def start(self):
        c = OsUtil("python").start("-m", "common.third_util.gunicorn_util")
        time.sleep(2)
        c.stop()


if __name__ == "__main__":
    GunicornUtil().run()
