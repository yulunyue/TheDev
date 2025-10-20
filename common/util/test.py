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

    def __init__(self, raise_err=False) -> None:
        self.prepare()
        self.raise_err = raise_err

    def prepare(self, args=None):
        pass

    def run(self, args=None):

        if args is None:
            args = sys.argv[1:]
        self.argvs, self.kw = url_to_json(args)
        if self.argvs:
            f = getattr(self, self.argvs[0], None)
            if f is None and self.argvs:
                f = getattr(self, f"test_{self.argvs[0]}")
            self.run_one_case(f, *self.argvs[1:], **self.kw)
        else:
            self.run_all_test()
        self.exit()

    def prepare_case(self, *args):
        pass

    def after_case(self, *args):
        pass

    def run_one_case(self, f, *args, **kw):
        self.prepare_case(*args)
        self.ep_cont = 0
        self.ok_count = 0
        start_time = time.time() * 1000
        self.fun_name = f.__name__
        logger.debug(f"---Test Begin {self.fun_name}------")
        msg = ""
        f(*args, **kw)
        end_time = time.time() * 1000
        logger.debug(
            f"---Test End {self.fun_name} [使用时间:{end_time-start_time} ms] [成功率:{self.ok_count}/{self.ep_cont}]---"
        )
        self.after_case(*args)
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
        d = Diff(expect_value).set_info(info)
        if d.is_same(a):
            self.ok_count += 1
        elif self.raise_err:
            raise Exception(a, expect_value)

    def get_temp_path(self, name):
        return f"data/test/{self.__class__.__name__}/{name}"

    def get_temp_file(self, name):
        path = self.get_temp_path(name)
        File(path).make_dir_if_not_exist()
        return path
