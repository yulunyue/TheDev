from common.service.export import Api, request_mock, API_CONFIG, get_proxy
import os
import sys

os.environ.setdefault("OUTBOUND_HTTP_PROXY", get_proxy("http"))
# os.environ.setdefault("EDGE_PORT_HTTP", "9999")
os.environ.setdefault("OUTBOUND_HTTPS_PROXY", get_proxy("https"))
request_mock()
sys.path.append("data/repo/localstack/localstack")
from localstack.services.install import installers

sqs = installers["sqs"]
installers.clear()
installers["sqs"] = sqs
from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase


class PyTestMain(ToolBase):
    def prepare(self, *args, **kw):
        self.u = PyTestUtil()

    def dev(self):
        aim1 = "data/repo/localstack/localstack/tests/integration/test_sqs.py::TestSqsProvider::test_create_fifo_queue_with_same_attributes_is_idempotent"
        self.u.set_flags(aim1).main()

    def dev1(self):
        aim1 = "tests/test_pytest.py"
        self.u.set_flags(aim1).main()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    PyTestMain().run()
