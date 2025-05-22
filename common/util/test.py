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

    def run(self, args=None):
        if args is None:
            args = sys.argv[1:]
        argvs, self.kw = url_to_json(args)
        f = getattr(self, f"test_{argvs[0]}")
        start_time = time.time() * 1000
        logger.info(f"---Test Begin {f.__name__}------")
        self.ep_cont = 0
        self.ok_count = 0
        f(*argvs[1:], **self.kw)
        end_time = time.time() * 1000
        logger.info(
            f"---Test End {f.__name__} [使用时间:{end_time-start_time} ms] [成功率:{self.ok_count}/{self.ep_cont}]---"
        )
        self.exit()

    def exit(self):
        pass

    def expect(self, a, expect_value, info=""):
        self.ep_cont += 1
        if a == expect_value or str(a) == str(expect_value):
            self.ok_count += 1
            return True
        logger.error(f"{a}!={expect_value} msg:{info}", stacklevel=2)
        return False

    def expect_array(self, src, dst, cha=0.001):
        if len(src) != len(dst):
            return self.expect(
                src, dst, info=f"array size is not same {len(src)}  {len(dst)} "
            )
        a = 0
        for i, v in enumerate(src):
            a += abs(v - dst[i])
        if a <= cha:
            return True
        logger.error(
            f"{a}>{cha}\nsrc={','.join(['%.2f'%v for v in src])}\ndst={','.join(['%.2f'%v for v in dst])}",
            stacklevel=2,
        )
        return False
