import sys
import time
from .fp import File
from .log import get_log, get_dev_log, logger
from .tool import url_to_json, md5, SYS_ARGS, SYS_KW, uid
from .module import Module, call_func_auto
from .difftool import Diff
from typing import Dict, List
import json
import os

TEST_FN_PREFIX = "test_"


class TestBase:
    TEST_EMABLE = True
    f = None
    setup_class_flag = False

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self):
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

    def expect(self, a, e=True, info="", stacklevel=2):
        if a != e:
            c = uid("case")
            get_dev_log(f"data/log/diff/{c}/i.txt").info(a)
            get_dev_log(f"data/log/diff/{c}/e.txt").info(e)

        assert a == e, f"{a}!={e}\n{info}"

    def expect_raise_error(self, fun, *args, error="", **kw):
        try:
            fun(*args, **kw)
        except Exception as e:
            self.expect(str(e), error)
        else:
            raise Exception("no error")
