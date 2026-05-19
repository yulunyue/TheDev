from ..tool import SYS_ARGS, SYS_KW, json_dumps, THE_DEV_LOGGER_PREFIX, dict_to_str
import sys

LOG_DIR = "data/log"

if THE_DEV_LOGGER_PREFIX in SYS_KW:
    LOG_DIR += f"/{SYS_KW.pop(THE_DEV_LOGGER_PREFIX)}"
LOG_MAP = dict()
LOGGER_MODE = "LOGGER_MODE"


def LOGGER_PREFIX(name):
    return f"{THE_DEV_LOGGER_PREFIX}={name}"


def name_to_path(name: str):
    name = name.replace(":", "_")
    if "/" not in name:
        path = LOG_DIR + "/" + name
    else:
        path = name
    if not path.endswith(".log"):
        path += ".log"
    return path


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
