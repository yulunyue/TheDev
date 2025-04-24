from common.util.export import TestBase
from common.service.export import ApiCall, Api, run, Task

import sys
import json
import _thread


class Test(TestBase):
    def test_http_by_thread(self):
        api = Api("http://127.0.0.1:9999")
        self.expect(
            api.post("/xx"),
            dict(statu=404, path="/xx", data=["/app/tmp/a/add", "/app/tmp/a/sub"]),
        )
        self.expect(api.post("/app/tmp/a/add", dict(a=1, b=2)), dict(c=3))
        self.expect(api.post("/app/tmp/a/sub", dict(a=1, b=2)), dict(c=-1))

    def test_http(self):
        _thread.start_new_thread(self.test_http_by_thread, ())
        run(
            dict(
                port=9999,
                py_modules={
                    "app/tmp": ["a"],
                },
            )
        )

    def test_task(self):
        Task().set_task(
            "test_task", Task.PY_MODULE_TYPE, ["app/tmp", "a", "task", 2]
        ).loop()

    def test_apicall(self):
        a = ApiCall()
        a.load_module_str("data", ["ylypy.a"])
        self.expect(a.call("/data/ylypy/a/add", dict(a=1, b=2)), dict(result=3))


if __name__ == "__main__":
    Test().run(sys.argv[1:])
