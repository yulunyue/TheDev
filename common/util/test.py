import sys
import time
from .fp import File
from .log import get_log, get_dev_log, logger
from .tool import url_to_json, md5, SYS_ARGS, SYS_KW
from .module import Module, call_func_auto
from .difftool import Diff
from typing import Dict, List
import json
import os

TEST_FN_PREFIX = "test_"


class Case:
    def __init__(self, path):
        self.path = path
        self.i = File(path + "/main.in").write_if_not_exists()
        self.o = File(path + "/main.out").write_if_not_exists()
        self.e = File(path + "/main.e").write_if_not_exists()

    def get_loger(self):
        return get_dev_log(self.path + "/main.log")

    def run_diff(self, result):
        self.o.write_file(result)
        e = None
        if self.e.exists():
            e = self.e.read_file()
        return Diff(e).is_same(result)

    def get_input(self):
        data = self.get_linput_lines()
        try:
            return json.loads(data)
        except Exception as e:
            return dict()

    def get_linput_lines(self):
        ret = self.i.read_file()
        return ret


class CaseFun:
    def __init__(self, name, f):
        self.ep_count = 0
        self.ok_count = 0
        self.f = f
        self.name = name
        self.fun_name = f.__name__

    def expect(self, a, expect_value, info, call):
        self.ep_count += 1
        msg = call(a, expect_value)
        if not msg:
            self.ok_count += 1
        else:
            self.error_logger.info(
                f"-----{self.ep_count}-----\rret:{a}\nexp:{expect_value}\ndiff:\n{msg}\n{info}"
            )
            logger.info(f"{a}!={expect_value}", stack_info=True)

    def run(self, *args, **kw):
        self.start_time = time.time()
        # self.error_logger = get_dev_log(f"data/test/error/{self.name}_{self.fun_name}")
        self.msg = ""
        self.f(*args, **kw)
        self.end_time = time.time()
        self.use_time = self.end_time - self.start_time


class TestBase:
    TEST_EMABLE = True
    f = None
    setup_class_flag = False

    @classmethod
    def setup_class(cls):
        pass

    def prepare_case(self, *args):
        pass

    def after_case(self, *args):
        pass

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

    def expect(self, a, expect_value=True, info="", stacklevel=2):
        assert a == expect_value, f"{a}!={expect_value}\n{info}"
