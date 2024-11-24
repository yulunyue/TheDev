import logging
from common.constant import Constant
from common.util.fp import File
LOG_MAP = dict()


class Logger(logging.Logger):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.path=f'./data/log/{name}.log'
        fp=File(self.path)
        if not fp.exists():
            fp.write_file('')
        self.add_hander(logging.FileHandler(
            self.path, mode='w'), logging.INFO)
        self.info("---start---log---")
        #self.add_hander(logging.StreamHandler(), logging.INFO)

    def add_hander(self, h: logging.Handler, level):
        fm = logging.Formatter(''.join([
            "[%(asctime)s]",
            # "levelname",
            # "process)s:%(threadName",
            "[%(filename)-10s]",
            "[%(lineno)-3s]",
            "[%(funcName)-12s] ",
            "%(message)-4s"
        ]))
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
