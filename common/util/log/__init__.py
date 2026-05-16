from .logger import get_log, Logger
from .the_dev_log import get_dev_log, TheDevLogger
from .util import LOGGER_PREFIX

logger = get_log("run")
log = get_dev_log("log")
log1 = get_dev_log("log1")
log2 = get_dev_log("log2")


def log_call(call, args):
    from ..fp import File

    f = File("data/tmp.json")
    fun = getattr(call(), args[0])(*args[1:])
    logger.info(f.write_file(fun))
