from common.util.test import TestBase
from common.util.tool import write_file
from common.service.http import run, DEFAULT_CONF_PATH, stop
from common.service.api import Api
import json
import _thread


class Test(TestBase):
    def test_http(self):
        api = Api("http://127.0.0.1:9999")
        # self.expect(api.post("/xx"), dict(statu=404,
        #             path="/xx", data=["/data/tmp/a/add"]))
        self.expect(api.post("/data/tmp/a/add", dict(a=1, b=2)), dict(c=3))
        self.expect(api.post("/data/tmp/a/sub", dict(a=1, b=2)), dict(c=-1))


def pre_pare():
    write_file(DEFAULT_CONF_PATH, dict(
        port=9999,
        py_modules={
            "data/tmp": ["a"]
        }
    ))
    write_file("data/tmp/util/fun.py", '''
def sub(self,a,b):
    return dict(c=a-b)
    ''')
    write_file("data/tmp/a.py", '''
from util.fun import sub
class Route:
    def add(self,a,b):
        return dict(c=a+b)
    def sub(self,a,b):
        return dict(c=a-b)
    ''')


if __name__ == "__main__":
    pre_pare()
    _thread.start_new_thread(Test().run, ())
    run()
