import sys
import threading
import time

import traceback
from ..fp import File
from ..log import logger
from .fm_info import FmInfo, FrameType
import math


class ThreadRecord(threading.Thread):

    def __init__(self) -> None:
        super().__init__(target=self.exec)
        self.error_msg = ""
        self.result = None

    def init(self):
        pass

    def run(self) -> None:
        self.state = 0
        sys.settrace(self.globaltrace)
        try:
            super().run()
        except Exception as e:
            self.error_msg = str(e)
            traceback.print_exc()
        self.state = 1

    def exec(self):
        self.result = self.exec_main(*self.args, **self.kw)

    def hander_frame(info: FmInfo):
        print(info.frame.f_code)

    def globaltrace(self, frame, event, arg):
        return self.localtrace

    def set_layout(self, keys):
        self._layout_keys = keys
        self._last_state = dict()
        for k in keys:
            self._last_state.update(self.get_current_value(k))
        return self

    def get_current_value(self, key):
        v = getattr(self.ins, key)
        if hasattr(v, "thread_current_view"):
            return v.thread_current_view(key)
        return {key: v}

    def localtrace(self, frame, event, arg):
        if event == "return":
            return self.localtrace

        for k in self._layout_keys:
            value_map = self.get_current_value(k)
            for key, current_value in value_map.items():

                if current_value != self._last_state[key]:
                    self.records.append(dict(key=key, value=current_value))
                    self._last_state[key] = current_value
                    return self.localtrace
        return self.localtrace

    def get_records(self):
        return self.records

    def execute(self, *args, **kw) -> "ThreadRecord":
        self.state = 0
        self.records = []
        self.msgs = []
        self.args = args
        self.kw = kw
        self.init()
        self.start()
        while not self.state:
            time.sleep(0.1)
        return self

    def exec_main(self, *args, **kw):
        return self.ins.exec(**self.kw)

    def cli(self, path="data/log/thread_view.log", *args, **kw):
        from common.third_util.pynut_util import PU_UTIL

        self.execute(*args, **kw)
        self.idx = 0

        def show():
            File(path).write_file(self.msgs[self.idx])

        def left():
            self.idx = (self.idx + len(self.msgs) - 1) % len(self.msgs)
            show()

        def right():
            self.idx = (self.idx + 1) % len(self.msgs)
            show()

        show()
        PU_UTIL.register(left=left, right=right).run()

    def get_layout(self):
        from common.tool.export import FontBase, Row, Column, to_web_view

        n = len(self._layout_keys)
        m = math.ceil(math.sqrt(n))
        r = Row()

        for i, k in enumerate(self._layout_keys):
            if i % m == 0:
                c = Column()
                r.add(c)
            c.add(to_web_view(k, getattr(self.ins, k)))
        return r

    def set_ins(self, ins):
        self.ins = ins
        return self

    def set_exec(self, fun):
        self.exec_fun = fun
        return self
