import sys
import threading
import time
from types import FrameType


def test_fun(n):
    RECORD_ENABLE = True
    time.sleep(2)
    ret = 0
    for i in range(n):
        ret += i
    return ret


class FmInfo:
    def __init__(self, frame) -> None:
        self.frame: FrameType = frame

    def get_locals(self):
        locals_var = self.frame.f_locals
        if not ThreadUtil.RECORD_ENABLE in locals_var:
            return
        ret = dict()
        for k in locals_var:
            if k == ThreadUtil.RECORD_ENABLE or k == 'self':
                continue
            ret[k] = locals_var[k]
        return ret


class ThreadUtil(threading.Thread):
    RECORD_ENABLE = 'RECORD_ENABLE'

    def __init__(self, target=None, kwargs=None) -> None:
        super().__init__(target=target, kwargs=kwargs)
        self.records = []

    def run(self) -> None:
        sys.settrace(self.globaltrace)
        super().run()
        self.state = 1

    def hander_frame(info: FmInfo):
        print(info.frame.f_code)

    def globaltrace(self, frame, event, arg):
        return self.localtrace

    def localtrace(self, frame, event, arg):
        info = FmInfo(frame).get_locals()
        if info:
            self.records.append(info)
        return self.localtrace

    def get_record(self):
        self.state = 0
        self.start()
        while not self.state:
            time.sleep(0.1)
        return self.records

    def test(self):
        pass


def run_watch_fun(fun, **kg):
    u = ThreadUtil(target=fun, kwargs=kg)
    return u.get_record()


def test():
    return run_watch_fun(test_fun, n=4)


if __name__ == "__main__":
    print(test())
