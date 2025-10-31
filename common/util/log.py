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

DEBUG_FMT = "%(message)s"


def name_to_path(name):
    if "/" not in name:
        path = f"{LOG_DIR}/{name}"
    else:
        path = name
    if not path.endswith(".log"):
        path += ".log"
    return path


def dict_to_str(kw: dict, indent=None):
    if indent is not None:
        return json_dumps(kw)
    ret = []
    for k, v in kw.items():
        ret.append(f"{'%s'%k}:{v}")
    return " ".join(ret)


class Logger(logging.Logger):

    def __init__(self, name, fmt, mode="w") -> None:
        super().__init__(name)
        self.cache_msgs = []
        self.path = name_to_path(name)
        self.fp = File(self.path).make_dir_if_not_exist()
        self.add_file_hander(fmt, mode)
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_file_hander(self, fmt, mode):
        self.add_hander(
            logging.FileHandler(
                self.path,
                mode=os.environ.get(LOGGER_MODE, mode),
                encoding="utf-8",
            ),
            logging.DEBUG,
            fmt=DEBUG_FMT,
        )

    def get_and_clear_cache(self):
        ret = self.cache_msgs[:]
        self.cache_msgs.clear()
        return "\n".join([str(v) for v in ret])

    def map(self, indent=None, **kw):
        self.debug(dict_to_str(kw, indent=indent), stacklevel=2)

    def info(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):

        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel + 1,
            extra=extra,
        )

    def add_hander(self, h: logging.Handler, level, fmt=None):
        if fmt is None:
            fmt = DEFAULT_FMT
        elif fmt == "":
            fmt = "%(message)s"
        fm = logging.Formatter(fmt, datefmt="%H:%M:%S")
        h.setFormatter(fm)
        h.setLevel(level)
        self.addHandler(h)


class TheDevLoger:
    def __init__(self, name, *args, **kw):
        self.fp = File(name_to_path(name)).write_file("")
        logger.info(self.fp.path, stacklevel=3)

    def get_writer(self):
        return self.fp.get_writer()

    def write(self, msg):
        w = self.fp.get_writer()
        w.write(f"{msg}\n")
        w.flush()

    def info(self, msg):
        self.write(msg)

    def debug(self, msg):
        self.write(msg)

    def exception(self, msg):
        self.write(msg)
        self.write("\n".join(traceback.format_stack()))

    def map(self, indent=None, **kw):
        self.info(dict_to_str(kw, indent=indent))


def get_dev_log(name) -> TheDevLoger:
    if name not in LOG_MAP:
        LOG_MAP[name] = TheDevLoger(name)
    return LOG_MAP[name]


def get_log(name="", fmt=None, mode="w") -> Logger:
    if name not in LOG_MAP:
        l = Logger(name, fmt, mode=mode)
        LOG_MAP[name] = l
        l.info(l.path, stacklevel=2)
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


logger = get_log("test")
