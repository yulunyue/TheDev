import sys
import threading
import time

import traceback
from ..fp import File
from ..log import logger
from .fm_info import FmInfo, FrameType


class ThreadRecord(threading.Thread):

    def __init__(self) -> None:
        super().__init__(target=self.exec)
        self.error_msg = ""
        self.result = None

    def format(self):
        return self.uk()

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

    _last_state = None

    def localtrace(self, frame, event, arg):
        if event == "return":
            return self.localtrace
        # print(frame, event, arg)
        state = self.uk()
        if state != self._last_state:
            # print(f"{state},{self._last_state},{self.to_josn()}")
            self.msgs.append(self.format())
            self.records.append(self.to_josn())
        self._last_state = state
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
        return self.exec_fun(**self.kw)

    def to_josn(self):
        return dict()

    def uk(self):
        return ""

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

    def set_exec(self, fun):
        self.exec_fun = fun
        return self
