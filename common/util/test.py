import sys
import time
from common.util.log import get_log
from common.util.tool import url_to_json

logger = get_log("test")
TEST_FN_PREFIX = "test_"


class TestBase:
    def __init__(self) -> None:
        self.prepare()

    def prepare(self):
        pass

    def run(self, args):
        argvs, self.kw = url_to_json(args)
        if not argvs:
            fns = [getattr(self, k) for k in dir(self) if k.startswith(TEST_FN_PREFIX)]
        else:
            fns = [getattr(self, TEST_FN_PREFIX + k) for k in argvs]
        for f in fns:
            start_time = time.time() * 1000
            logger.info(f"---Test Begin {f.__name__}------")
            self.ep_cont = 0
            f()
            end_time = time.time() * 1000
            logger.info(
                f"---Test End {f.__name__} [ut:{end_time-start_time} ms] [ep:{self.ep_cont}]---"
            )
        self.exit()

    def exit(self):
        pass

    def expect(self, a, expect_value, info=""):
        self.ep_cont += 1
        if a == expect_value or str(a) == str(expect_value):
            return True
        logger.error(f"{a}!={expect_value} msg:{info}", stacklevel=2)
        return False
