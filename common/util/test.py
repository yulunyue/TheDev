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
        self.error_logger = get_dev_log(f"data/test/error/{self.name}_{self.fun_name}")
        self.msg = ""
        self.f(*args, **kw)
        self.end_time = time.time()
        self.use_time = self.end_time - self.start_time


class TestBase:
    TEST_EMABLE = True
    f = None

    def prepare(self, args=None):
        pass

    def run(self, args=None):
        self.prepare()
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
        logger.info(
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
        if self.f:
            self.f.expect(a, expect_value, info, lambda a, dst: Diff(a).is_same(dst))
        else:
            assert a == expect_value

    def get_temp_path(self, name):
        return f"data/test/{self.__class__.__name__}/{name}"

    def get_temp_file(self, name):
        path = self.get_temp_path(name)
        File(path).make_dir_if_not_exist()
        return path


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


def make_md_file(key=None, msg=""):
    if key is None:
        file_dir = (
            sys.argv[0]
            .replace(os.getcwd() + "\\", "")
            .replace(".py", ".md")
            .replace("\\", "/")
        )
    else:
        file_dir = key + ".md"
    f = File(file_dir)
    f.write_if_not_exists(msg)
    return f.path, "\n".join(f.read_line()[-5:])


class ToolBase:
    name = None

    @property
    def logger(self):
        return get_log(f"tool/{self.get_name()}.log")

    @property
    def dev_log(self):
        return get_dev_log(f"tool/{self.get_name()}_dev.log")

    def prepare(self, *args):
        pass

    def get_name(self):
        return self.name or self.__class__.__name__

    def exit(self):
        pass

    def run(self):
        self.msgs = []
        self.argvs, self.kw = SYS_ARGS.copy(), SYS_KW.copy()
        fun_name = self.argvs.pop()
        self.prepare(*self.argvs)
        f = getattr(self, fun_name, None)
        if f is None:
            logger.info(
                [
                    v
                    for v in list(dir(self))
                    if not v[0] == "_" and callable(getattr(self, v, None))
                ]
            )
            self.exit()
            return

        f(**self.kw)
        md_file = make_md_file()[0]
        self.logger.info(md_file)
        self.logger.info(md_file.replace(".md", ".py"))
        self.exit()

    def cli(self):
        fi, fo = self.get_temp_file("inp.txt"), self.get_temp_file("out.txt")
        fi.write_if_not_exists("")
        last_cmd = []
        out_put_msgs = dict()
        while True:
            time.sleep(1)
            cmd = [
                v
                for v in fi.read_fast_file().split("\n")
                if v and not v.startswith("#")
            ]
            if cmd == last_cmd:
                continue
            flag = False
            for i, v in enumerate(cmd):
                if i < len(last_cmd) and v == last_cmd[i]:
                    continue
                out_put_msgs[i] = [i, v, self.do_cmd(*v.split(" "))]
                flag = True
            if flag:
                msgs = []
                sr = sorted(out_put_msgs.values())[: len(cmd)]
                for i, v, r in sr:
                    msgs.append(f"i:{i} , cmd:{v}\n----------\n{r}\n-----------")
                fo.write_file("\n".join(msgs))
            last_cmd = cmd

    def do_cmd(self, *cmd):
        pass

    def info(self, msg):
        self.msgs.append(msg)

    def get_temp_file(self, name):
        path = f"data/tool/{self.__class__.__name__}/{name}"
        logger.info(path)
        return File(path)
