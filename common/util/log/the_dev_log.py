from ..fp import File
from .util import name_to_path, LOG_MAP, dict_to_str
from typing import List, Dict


class TheDevLogger:
    def __init__(self, name, *args, **kw):
        self.name = name
        self._fp = None

    @property
    def fp(self):
        if self._fp is None:
            from ..log import logger

            self._fp = File(name_to_path(self.name)).write_file("")
            logger.info(self.fp, stacklevel=3)
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

    def clear(self):
        w = self.fp.get_writer()
        w.seek(0)
        w.truncate()
        w.flush()
        return self

    def info(self, msg):
        self.write(msg)

    def warning(self, msg):
        self.write(msg)

    def debug(self, msg):
        self.write(msg)

    # def exception(self, msg):
    #     self.write(msg)
    #     self.write("\n".join(traceback.format_stack()))

    def log_tree(self, g: List[List[int]], f=None, head=0):
        from ...tool.str_util import StrUtil
        from common.third_util.view.pygraphviz_util import PyGraphViz

        if isinstance(g, list):
            self.write(StrUtil().format_g_tree(g, f, head=head))
        elif isinstance(g, dict):
            PyGraphViz().load(self.fp.path + ".png").draw(**g)

    def map(self, indent=" ", **kw):
        self.info(dict_to_str(**kw, indent=indent))


def get_dev_log(name) -> TheDevLogger:
    LOG_MAP[name] = TheDevLogger(name)
    return LOG_MAP[name]
