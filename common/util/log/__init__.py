from .logger import get_log, Logger
from .the_dev_log import get_dev_log, TheDevLoger
from .util import LOGER_PREFIX

logger = get_log("run")
log = get_dev_log("log")
log1 = get_dev_log("log1")
log2 = get_dev_log("log2")
