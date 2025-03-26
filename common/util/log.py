import logging
import logging.handlers
import os
from common.constant import Constant
from common.util.fp import File


LOG_MAP = dict()
LOGGER_MODE = "LOGGER_MODE"


class ImmediateFileHandler(logging.FileHandler):
    def emit(self, record):
        # 调用父类的emit方法写入日志
        super().emit(record)
        # 强制刷新流缓冲区
        self.stream.flush()

    # def _open(self):
    #     # 设置buffering=1（行缓冲）或0（无缓冲，需二进制模式）
    #     return open(self.baseFilename, self.mode, encoding=self.encoding, buffering=0)


class Logger(logging.Logger):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.path = f"./data/log/{name}.log"

        fp = File(self.path)
        if not fp.exists():
            fp.write_file("")

        self.add_hander(
            ImmediateFileHandler(
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
                    "[%(pathname)-10s:%(lineno)-3s]",
                    "[%(funcName)-12s] ",
                    "%(message)-4s",
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
