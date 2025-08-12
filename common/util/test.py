import sys
import time
from common.util.fp import File
from common.util.log import get_log
from common.util.tool import url_to_json
from common.util.difftool import Diff
from typing import Dict, List

logger = get_log("test")
TEST_FN_PREFIX = "test_"


class TestBase:
    TEST_EMABLE = True
    RAISE_ERROR = True

    def __init__(self) -> None:
        self.prepare()

    def prepare(self, args=None):
        pass

    def run(self, args=None):

        if args is None:
            args = sys.argv[1:]
        self.argvs, self.kw = url_to_json(args)
        self.prepare_case(*self.argvs)
        f = getattr(self, self.argvs[0], None)
        if f is None:
            f = getattr(self, f"test_{self.argvs[0]}")
        self.run_one_case(f, *self.argvs[1:], **self.kw)
        self.after_case(*self.argvs)

    def prepare_case(self, *args):
        pass

    def after_case(self, *args):
        pass

    def run_one_case(self, f, *args, **kw):
        self.ep_cont = 0
        self.ok_count = 0
        start_time = time.time() * 1000
        logger.info(f"---Test Begin {f.__name__}------")
        msg = ""
        f(*args, **kw)
        end_time = time.time() * 1000
        logger.info(
            f"---Test End {f.__name__} [使用时间:{end_time-start_time} ms] [成功率:{self.ok_count}/{self.ep_cont}]---"
        )
        return msg

    def run_all_test(self):
        for key in dir(self):
            if not key.startswith("test_"):
                continue
            f = getattr(self, key)
            if not callable(f):
                continue
            s = self.run_one_case(f)
            if s:
                return s

    def exit(self):
        pass

    def expect(self, a, expect_value=True, info="", stacklevel=2):
        self.ep_cont += 1
        is_eq = a == expect_value or str(a) == str(expect_value)
        if is_eq:
            self.ok_count += 1
            return True
        msg = f"\ninfo:\n{info}\nresult:\n{a}\nexpect:\n{expect_value}"
        if self.RAISE_ERROR:
            raise Exception(msg)
        logger.info(
            msg,
            stacklevel=stacklevel,
        )
        return False

    def expect_dfs(self, src, dst, info=""):
        msg = Diff(src).compare(dst)
        return self.expect(len(msg), 0, info + "\n".join(msg), stacklevel=3)

    def expect_ndarray(self, a, e, wucha=0.000001):
        import numpy as np

        if not isinstance(a, np.ndarray):
            a = np.array(a)
        if not isinstance(e, np.ndarray):
            e = np.array(e)
        if a.shape != e.shape:
            not_equ = True
        else:
            not_equ = abs(a - e).sum() > wucha
        return self.expect(
            not_equ,
            False,
            info=f"shape:{a.shape}\n{a}\n!=\nshape:{e.shape}\n{e}",
            stacklevel=3,
        )

    def get_temp_file(self, name):
        path = f"data/test/{self.__class__.__name__}/{name}"
        File(path).make_dir_if_not_exist()
        return path
