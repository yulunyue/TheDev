import logging
import logging.handlers
import os
from common.constant import Constant
from common.util.fp import File
import sys
import traceback

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

    def __init__(self, name, fmt) -> None:
        super().__init__(name)
        self.path = f"{LOG_DIR}/{name}.log"
        self.add_hander(
            logging.FileHandler(
                self.path, mode=os.environ.get(LOGGER_MODE, "a+"), encoding="utf-8"
            ),
            logging.INFO,
            fmt=fmt,
        )
        self.first_log = True
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def info(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=2, extra=None
    ):
        if self.first_log:
            File(self.path).write_file("")
            self.first_log = False
        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def table(self, datas: dict, key=None, header_key="t_name"):
        from prettytable import PrettyTable

        headers = [header_key] + list(list(datas.values())[0].keys())
        for k, v in datas.items():
            v[header_key] = k
        datas = list(sorted(datas.values(), key=key))
        tb = PrettyTable(field_names=headers)
        for row in datas:
            tb.add_row([row[k] for k in headers])
        self.info(f"-TABLLE-\n{tb}")

    def add_hander(self, h: logging.Handler, level, fmt=None):
        if fmt is None:
            fmt = DEFAULT_FMT
        if fmt:
            fm = logging.Formatter(fmt)
            h.setFormatter(fm)
        h.setLevel(level)
        self.main_hander = h
        self.addHandler(h)


class TheDevLoger:
    def __init__(self, name):
        self.path = f"./data/log/{name}.log"
        self.fp = open(self.path, "w", encoding="utf-8")

    def info(self, msg):
        self.fp.write(str(msg) + "\n")
        self.fp.flush()


def get_log(name="", log_class="log", fmt=None) -> Logger:
    if name not in LOG_MAP:
        LOG_MAP[name] = {"default": TheDevLoger, "log": Logger}[log_class](name, fmt)
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
