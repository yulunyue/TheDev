import logging
import logging.handlers
import sys
from .util import name_to_path, LOGGER_MODE, dict_to_str, LOG_MAP
from ..fp import File
import os
from ...constant import C

_STACKLEVEL_SUPPORT = sys.version_info >= (3, 8)

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


class Logger(logging.Logger):

    def __init__(self, name, fmt, mode="w") -> None:
        super().__init__(name)
        self.cache_msgs = []
        self.path = name_to_path(name)
        self.fp = File(self.path).make_dir_if_not_exist()
        self.add_file_hander(fmt, mode)
        self.add_hander(logging.StreamHandler(), logging.INFO)
        self.log_call_hock = None

    def set_log_call_hock(self, log_call_hock):
        self.log_call_hock = log_call_hock
        return self

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
        self.info(dict_to_str(indent=indent, **kw), stacklevel=2)

    def debug(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        if _STACKLEVEL_SUPPORT:
            return super().debug(
                msg, *args, exc_info=exc_info, stack_info=stack_info,
                stacklevel=stacklevel + 1, extra=extra,
            )
        return super().debug(
            msg, *args, exc_info=exc_info, stack_info=stack_info, extra=extra,
        )

    def info(self, msg, *args, stacklevel=1, extra=None):
        if extra:
            from ..io.manage import IO_MANAGE

            IO_MANAGE.send(extra, msg)
        if _STACKLEVEL_SUPPORT:
            return super().info(msg, *args, stacklevel=stacklevel + 1)
        return super().info(msg, *args)

    def add_hander(self, h: logging.Handler, level, fmt=None):
        if fmt is None:
            fmt = DEFAULT_FMT
        elif fmt == "":
            fmt = "%(message)s"
        fm = logging.Formatter(fmt, datefmt="%H:%M:%S")
        h.setFormatter(fm)
        h.setLevel(level)
        self.addHandler(h)


def get_log(name="", fmt=None, mode="w") -> Logger:
    if name not in LOG_MAP:
        l = Logger(name, fmt, mode=mode)
        l.info(l.path, stacklevel=2)
        LOG_MAP[name] = l
    return LOG_MAP[name]
