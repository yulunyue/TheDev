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

    def get_info_dict(self):
        return dict(
            f_lineno=self.frame.f_lineno,
            f_locals=self.frame.f_locals
        )


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
        info = FmInfo(frame).get_info_dict()
        if info['f_locals'].get(self.RECORD_ENABLE):
            # info['f_locals'].pop(self.RECORD_ENABLE)
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


def run_watch_fun():
    u = ThreadUtil(target=test_fun, kwargs=dict(n=4))
    return u.get_record()


def test():
    return run_watch_fun()


if __name__ == "__main__":
    print(test())
