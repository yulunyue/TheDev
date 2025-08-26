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
        "[%(funcName)s]",
        " %(message)s",
    ]
)


class Logger(logging.Logger):

    def __init__(self, name, fmt=None, mode="w") -> None:
        super().__init__(name)
        self.cache_msgs = []
        self.cache_enable = False
        self.path = f"{LOG_DIR}/{name}"
        File(self.path).make_dir_if_not_exist()
        self.add_file_hander(fmt, mode)
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_file_hander(self, fmt, mode):
        self.add_hander(
            logging.FileHandler(
                self.path + ".log",
                mode=os.environ.get(LOGGER_MODE, mode),
                encoding="utf-8",
            ),
            logging.DEBUG,
            fmt=fmt,
        )

    def enable_cache(self):
        self.cache_enable = True
        return self

    def get_and_clear_cache(self):
        ret = self.cache_msgs[:]
        self.cache_msgs.clear()
        return "\n".join([str(v) for v in ret])

    def map(self, indent=None, **kw):
        ret = []
        for k, v in kw.items():
            ret.append(f"{'%s'%k}:{v}")
        if indent is None:
            self.info(" ".join(ret), stacklevel=2)
        else:
            self.info(json_dumps(kw, indent=indent))

    def info(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        if self.cache_enable:
            self.cache_msgs.append(str(msg))
            return
        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel + 1,
            extra=extra,
        )

    def draw_line(self, name, data):
        from common.tool.draw import Draw

        save_path = f"{LOG_DIR}/line/{self.name}_{name}.svg"
        Draw().draw_line(data).save(save_path)

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
