import logging
from common.constant import Constant
LOG_MAP = dict()


class Logger(logging.Logger):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.add_hander(logging.FileHandler(
            f'./data/log/{name}.log', mode='w'), logging.NOTSET)
        # self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_hander(self, h: logging.Handler, level):
        fm = logging.Formatter("[%("+')s] [%('.join([
            "asctime",
            "levelname",
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


logger = get_log(Constant.APP_NAME)


def test():
    logger.info("xx")
    logger.error("abc", stack_info=True)
    # log.critical("aa", stack_info=True)


if __name__ == "__main__":
    test()
