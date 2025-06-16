import logging
import logging.handlers
import os
from common.constant import Constant
from common.util.fp import File
import sys
import traceback
from common.util.tool import json_dumps

LOG_DIR = "data/log"
JSON_TMP_FILE = File(f"{LOG_DIR}/tmp.json")
LOG_MAP = dict()
LOGGER_MODE = "LOGGER_MODE"

DEFAULT_FMT = "".join(
    [
        "[%(asctime)s]",
        # "levelname",
        # "process)s:%(threadName",
        "[%(pathname)s:%(lineno)s]",
        "[%(funcName)s] ",
        "%(message)s",
    ]
)


class Logger(logging.Logger):

    def __init__(self, name, fmt, mode="w") -> None:
        super().__init__(name)
        self.msgs = []
        self.path = f"{LOG_DIR}/{name}"
        self.add_hander(
            logging.FileHandler(
                self.path + ".log",
                mode=os.environ.get(LOGGER_MODE, mode),
                encoding="utf-8",
            ),
            logging.INFO,
            fmt=fmt,
        )
        self.add_hander(
            logging.FileHandler(
                self.path + "_debug.log",
                mode=os.environ.get(LOGGER_MODE, mode),
                encoding="utf-8",
            ),
            logging.DEBUG,
            fmt=fmt,
        )
        File(self.path).make_dir_if_not_exist()
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def get_tmp_msgs(self):
        ret = self.msgs[:]
        self.msgs.clear()
        return ret

    def pt(self, msg):
        self.msgs.append(msg)
        return self

    def map(self, indent=None, **kw):
        ret = []
        for k, v in kw.items():
            ret.append(f"{'%s'%k}:{v}")
        if indent is None:
            self.info(" ".join(ret), stacklevel=2)
        else:
            self.info(json_dumps(kw, indent=indent))

    def table(self, datas: dict, key=None, header_key="t_name"):
        from prettytable import PrettyTable

        headers = [header_key] + list(list(datas.values())[0].keys())
        for k, v in datas.items():
            v[header_key] = k
        datas = list(sorted(datas.values(), key=key))
        tb = PrettyTable(field_names=headers)
        for row in datas:
            tb.add_row([row[k] for k in headers])
        self.info(f"-TABLLE-\n{tb}", stacklevel=2)

    def draw_line(self, name, data):
        from common.tool.draw import Draw

        Draw().draw_line(data).save(f"{LOG_DIR}/{self.name}_{name}.svg")

    def add_hander(self, h: logging.Handler, level, fmt=None):
        if fmt is None:
            fmt = DEFAULT_FMT
        elif fmt == "":
            fmt = "%(message)s"
        fm = logging.Formatter(fmt)
        h.setFormatter(fm)
        h.setLevel(level)
        self.addHandler(h)


class TheDevLoger:
    def __init__(self, name):
        self.path = f"./data/log/{name}.log"
        self.fp = open(self.path, "w", encoding="utf-8")

    def info(self, msg):
        self.fp.write(str(msg) + "\n")
        self.fp.flush()


def get_log(name="", log_class="log", fmt=None, mode="w") -> Logger:
    if name not in LOG_MAP:
        LOG_MAP[name] = {"default": TheDevLoger, "log": Logger}[log_class](
            name, fmt, mode=mode
        )
    return LOG_MAP[name]


def std_mock(with_trace=True):
    old_std = sys.stdout
    old_error = sys.stderr
    log = get_log("std", fmt="")

    class Tmp:
        data = ""

        def write(self, data: str):
            self.data += data
            # raise Exception(data)
            if self.data.endswith("\n"):
                if with_trace:
                    stack_str = traceback.format_stack()
                    log.info("".join(stack_str), stacklevel=-1)
                    log.info(f"{self.data[:-1]}", stacklevel=3)
                else:
                    log.info(self.data[:-1])
                self.data = ""

        def flush(self):
            old_error.flush()

    sys.stdout = Tmp()
    # sys.stderr = sys.stdout
