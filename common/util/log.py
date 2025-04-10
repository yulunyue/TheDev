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


class Logger(logging.Logger):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.path = f"{LOG_DIR}/{name}.log"
        self.add_hander(
            logging.FileHandler(
                self.path, mode=os.environ.get(LOGGER_MODE, "w"), encoding="utf-8"
            ),
            logging.INFO,
        )

        # self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_hander(self, h: logging.Handler, level):
        fm = logging.Formatter(
            "".join(
                [
                    "[%(asctime)s]",
                    # "levelname",
                    # "process)s:%(threadName",
                    "[%(pathname)s:%(lineno)s]",
                    "[%(funcName)s] ",
                    "%(message)s",
                ]
            )
        )
        h.setLevel(level)
        h.setFormatter(fm)
        self.addHandler(h)


class TheDevLoger:
    def __init__(self, name):
        self.path = f"./data/log/{name}.log"
        self.fp = open(self.path, "w", encoding="utf-8")

    def info(self, msg):
        self.fp.write(str(msg) + "\n")
        self.fp.flush()


def get_log(name="", log_class="log") -> Logger:
    if name not in LOG_MAP:
        LOG_MAP[name] = {"default": TheDevLoger, "log": Logger}[log_class](name)
    return LOG_MAP[name]


def std_mock():
    old_std = sys.stdout
    old_error = sys.stderr

    class Tmp:

        def write(self, data):
            stack_str = traceback.format_stack()
            get_log("std").info(f"{stack_str}\n{data}")

        def flush(self):
            old_error.flush()

    sys.stdout = Tmp()


# std_mock()
