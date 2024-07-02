from common.util.test import TestBase
from .http import run, DEFAULT_CONF_PATH, start, stop
from .api import Api
import json


class Test(TestBase):
    def test_http(self):
        api = Api("http://127.0.0.1:9999")
        self.expect(api.post("/xx"), dict(statu=404,
                    path="/xx", data=["/data/tmp/a/add"]))
        self.expect(api.post("/data/tmp/a/add", dict(a=1, b=2)), dict(c=3))

    def exit(self):
        stop()


if __name__ == "__main__":
    # json.dump(dict(
    #     port=9999,
    #     py_modules={
    #         "data/tmp": ["a"]
    #     }
    # ), open(DEFAULT_CONF_PATH, 'w'), indent=4)
    # start(lambda: Test().run_with_error())
    Test().run()
