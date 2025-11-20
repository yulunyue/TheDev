from common.util.export import TestBase, logger
from common.service.export import Api, request_mock
import requests


class TestIo(TestBase):

    def test_requests(self):
        request_mock()
        res = requests.get("https://github.com")
        logger.debug(res)

    def debug(self):
        self.test_requests()


if __name__ == "__main__":
    TestIo().run()
