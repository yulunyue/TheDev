from common.util.test import TestBase
from common.third_util.gunicorn_util import GunicornUtil


class TestGunicorn(TestBase):
    def setup_class(self):
        GunicornUtil().start()


if __name__ == "__main__":
    TestGunicorn().run()
