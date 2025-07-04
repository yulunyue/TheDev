import sys
import time
from common.util.log import get_log
from common.util.tool import url_to_json
from common.util.difftool import Diff
from typing import Dict, List

logger = get_log("test")
TEST_FN_PREFIX = "test_"


class SolotionBase:
    _msg = []

    def get_cases(self) -> List[Dict]:
        return []

    def log(self, *args):
        msgs = " ".join([str(a) for a in args])
        self._msg.append(msgs)

    def get_msgs(self):
        ret = self._msg[:]
        self._msg.clear()
        return ret


class TestBase:
    def __init__(self) -> None:
        self.prepare()

    def prepare(self):
        pass

    def run(self, args=None):
        try:
            if args is None:
                args = sys.argv[1:]
            argvs, kw = url_to_json(args)
            self.run_one_case(argvs[0], argvs[1:], kw)
        except Exception as e:
            raise e
        finally:
            self.exit()

    def run_one_case(self, name, args, kw):
        f = getattr(self, f"test_{name}")
        start_time = time.time() * 1000
        logger.info(f"---Test Begin {f.__name__}------")
        self.ep_cont = 0
        self.ok_count = 0
        f(*args, **kw)
        end_time = time.time() * 1000
        logger.info(
            f"---Test End {f.__name__} [使用时间:{end_time-start_time} ms] [成功率:{self.ok_count}/{self.ep_cont}]---"
        )

    def exit(self):
        pass

    def expect(self, a, expect_value=True, info="", stacklevel=2):
        self.ep_cont += 1
        if not isinstance(a, list) and isinstance(expect_value, list):
            is_eq = a in expect_value
        else:
            is_eq = a == expect_value or str(a) == str(expect_value)
        if is_eq:
            self.ok_count += 1
            return True
        logger.error(
            f"info:{info} result:{a}!=expect:{expect_value}", stacklevel=stacklevel
        )
        return False

    def expect_dfs(self, src, dst):
        msg = Diff(src).compare(dst)
        return self.expect(len(msg), 0, "\n".join(msg), stacklevel=3)
