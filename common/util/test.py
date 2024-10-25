import sys
import time
from common.util.log import logger
TEST_FN_PREFIX = 'test_'


class TestBase:
    def __init__(self) -> None:
        self.prepare()

    def prepare(self):
        pass

    def run(self):
        if len(sys.argv) == 1:
            fns = [getattr(self, k)
                   for k in dir(self) if k.startswith(TEST_FN_PREFIX)]
        else:
            fns = [getattr(self, TEST_FN_PREFIX+k) for k in sys.argv[1:]]
        for f in fns:
            start_time = time.time()*1000
            logger.info(f'---Test Begin {f.__name__}------')
            self.ep_cont = 0
            f()
            end_time = time.time()*1000
            logger.info(
                f'---Test End {f.__name__} [ut:{end_time-start_time} ms] [ep:{self.ep_cont}]---')
        self.exit()

    def exit(self):
        pass

    def expect(self, a, b, info=""):
        self.ep_cont += 1
        if a == b or str(a) == str(b):
            return True
        raise Exception(f'{a}!={b} [{info}]')
