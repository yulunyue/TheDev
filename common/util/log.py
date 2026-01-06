import logging
import logging.handlers
import os
from .fp import File
from .tool import SYS_ARGS, SYS_KW, json_dumps, THE_DEV_LOGER_PREFIX
import sys
import traceback
from .str_util import StrUtil
from typing import List


def LOGER_PREFIX(name):
    return f"{THE_DEV_LOGER_PREFIX}={name}"


LOG_PREFIX = ""
LOG_DIR = "data/log"
JSON_TMP_FILE = File(f"{LOG_DIR}/tmp.json")
if THE_DEV_LOGER_PREFIX in SYS_KW:
    LOG_DIR += f"/{SYS_KW.pop(THE_DEV_LOGER_PREFIX)}"
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


def name_to_path(name: str):
    name = name.replace(":", "_")
    if "/" not in name:
        path = LOG_DIR + "/" + name
    else:
        path = name
    if not path.endswith(".log"):
        path += ".log"
    return path


def dict_to_str(kw: dict, indent=" "):
    if isinstance(indent, int):
        return json_dumps(kw, indent=indent)
    ret = [""]
    for k, v in kw.items():
        ret.append(f"{'%s'%k}: {v};")
    return indent.join(ret)


class Logger(logging.Logger):

    def __init__(self, name, fmt, mode="w") -> None:
        super().__init__(name)
        self.cache_msgs = []
        self.path = name_to_path(name)

        self.fp = File(self.path).make_dir_if_not_exist()
        self.add_file_hander(fmt, mode)
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def run_capture_error(self, f, *args, captures="", **kw):
        try:
            f(*args, **kw)
        except Exception as e:
            import traceback

            if captures and str(e).startswith(captures):
                s = [f"\nERROR_MSG:{e}\n"] + traceback.format_tb(e.__traceback__)
                self.debug("".join(s))
            else:
                raise Exception(e)

    def add_file_hander(self, fmt, mode):
        self.add_hander(
            logging.FileHandler(
                self.path,
                mode=os.environ.get(LOGGER_MODE, mode),
                encoding="utf-8",
            ),
            logging.DEBUG,
            fmt=fmt,
        )

    def get_and_clear_cache(self):
        ret = self.cache_msgs[:]
        self.cache_msgs.clear()
        return "\n".join([str(v) for v in ret])

    def map(self, indent=" ", **kw):
        self.info(dict_to_str(kw, indent=indent), stacklevel=2)

    def debug(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        return super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel + 1,
            extra=extra,
        )

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
        self.name = name
        self._fp = None

    @property
    def fp(self):
        if self._fp is None:
            self._fp = File(name_to_path(self.name)).write_file("")
            logger.info(self.fp, stacklevel=4)
        return self._fp

    def get_writer(self):
        return self.fp.get_writer()

    def write(self, msg):
        w = self.fp.get_writer()
        if isinstance(msg, str):
            msg = msg.encode("utf-8")
        elif not isinstance(msg, bytes):
            msg = str(msg).encode("utf-8")
        w.write(msg + b"\n")
        w.flush()

    def info(self, msg):
        self.write(msg)

    def debug(self, msg):
        self.write(msg)

    def exception(self, msg):
        self.write(msg)
        self.write("\n".join(traceback.format_stack()))

    def log_tree(self, g: List[List[int]], f, head=0):
        self.write(StrUtil().format_g_tree(g, f, head=head))

    def map(self, indent=" ", **kw):
        self.info(dict_to_str(kw, indent=indent))


def get_dev_log(name) -> TheDevLoger:
    if name not in LOG_MAP:
        LOG_MAP[name] = TheDevLoger(name)
    return LOG_MAP[name]


def get_log(name="", fmt=None, mode="w") -> Logger:
    if name not in LOG_MAP:
        l = Logger(name, fmt, mode=mode)
        l.info(l.path, stacklevel=2)
        LOG_MAP[name] = l
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
log = get_dev_log("log")
