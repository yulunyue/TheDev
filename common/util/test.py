import sys
import time
from common.util.fp import File
from common.util.log import get_log, get_dev_log
from common.util.tool import url_to_json
from common.util.difftool import Diff
from typing import Dict, List

logger = get_log("test")
TEST_FN_PREFIX = "test_"


class CaseFun:
    def __init__(self, name, f):
        self.ep_count = 0
        self.ok_count = 0
        self.f = f
        self.name = name
        self.fun_name = f.__name__

    def expect(self, a, expect_value, info):
        self.ep_count += 1
        result, msg = Diff(a).is_same(expect_value)
        if result:
            self.ok_count += 1
        else:
            self.error_logger.info(f"-----{self.ep_count}-----\n{msg}\n{info}")

    def run(self, *args, **kw):
        self.start_time = time.time()
        self.error_logger = get_dev_log(f"data/test/error/{self.name}_{self.fun_name}")
        self.msg = ""
        try:
            self.f(*args, **kw)
        except Exception as e:
            self.msg = str(e)
            self.error_logger.exception(e)
        self.end_time = time.time()
        self.use_time = self.end_time - self.start_time


class TestBase:
    TEST_EMABLE = True

    def __init__(self, raise_err=False) -> None:
        self.prepare()

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
        self.f = CaseFun(self.__class__.__name__, f)
        self.f.run(*args, **kw)
        pass_statu = (
            "pass"
            if self.f.ep_count > 0 and self.f.ok_count == self.f.ep_count
            else "fail"
        )
        logger.debug(
            f"run_test [{pass_statu} {self.f.ok_count}/{self.f.ep_count}] use_time[{'%05d'%int(self.f.use_time*1000)}] {self.__class__.__name__}::{f.__name__} {self.f.msg}"
        )
        self.after_case(*args)

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
        self.f.expect(a, expect_value, info)

    def get_temp_path(self, name):
        return f"data/test/{self.__class__.__name__}/{name}"

    def get_temp_file(self, name):
        path = self.get_temp_path(name)
        File(path).make_dir_if_not_exist()
        return path
