import sys
import threading
import time
from types import FrameType
import traceback

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

    def get_local_self(self):
        return self.frame.f_locals['self']


class ThreadRecord(threading.Thread):

    def __init__(self, target, record_fun) -> None:
        super().__init__(target=target)
        self.record_fun = record_fun
        self.records = []
        self.error_msg=""
    def run(self) -> None:
        sys.settrace(self.globaltrace)
        try:
            super().run()
        except Exception as e:
            self.error_msg = str(e)
            traceback.print_exc()
        self.state = 1

    def hander_frame(info: FmInfo):
        print(info.frame.f_code)

    def globaltrace(self, frame, event, arg):
        return self.localtrace

    def localtrace(self, frame, event, arg):
        if event == 'return':
            return self.localtrace
        info = self.record_fun()
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


def run_watch_fun(exec_fun, record_fun):
    u = ThreadRecord(exec_fun, record_fun)
    return u.get_record(),u.error_msg


def test():
    return run_watch_fun(test_fun, n=4)


if __name__ == "__main__":
    print(test())
