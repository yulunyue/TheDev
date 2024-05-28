import logging
from common.constant import Constant
LOG_MAP = dict()


class Logger(logging.Logger):
    def __init__(self, name) -> None:
        super().__init__(name)
        # self.add_hander(logging.FileHandler(
        #     f'../data/{name}.log', mode='w'), logging.NOTSET)
        self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_hander(self, h: logging.Handler, level):
        fm = logging.Formatter("[%("+')s] [%('.join([
            "asctime",
            "process)s:%(threadName",
            "pathname)s:%(lineno",
            "funcName",
            "message"
        ])+")s]")
        h.setLevel(level)
        h.setFormatter(fm)
        self.addHandler(h)


def get_log(name="") -> Logger:
    if name not in LOG_MAP:
        LOG_MAP[name] = Logger(name)
    return LOG_MAP[name]


log = get_log(Constant.APP_NAME)
