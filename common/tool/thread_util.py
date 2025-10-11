import sys
import threading
import time
from types import FrameType
import traceback
from common.util.export import logger


class FmInfo:
    def __init__(self, frame) -> None:
        self.frame: FrameType = frame

    def get_local_self(self):
        return self.frame.f_locals["self"]


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
        raise Exception("todo")

    def to_josn(self):
        raise Exception("todo")

    def log(self):
        for r in self.records:
            logger.map(**r)

    def uk(self):
        return ""

    def cli(self, path, *args, **kw):
        self.execute()


class TestRc(ThreadRecord):
    def init(self):
        self.a = 0
        self.b = 0

    def exec_main(self):
        for _ in range(3):
            self.a += 1
            self.b += 1
        return self.a

    def uk(self):
        return f"{self.a}"

    def to_josn(self):
        return dict(a=self.a, b=self.b)
