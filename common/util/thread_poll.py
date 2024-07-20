
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import time


class ThreadExecError:
    def __init__(self, msg) -> None:
        self.msg = msg


class ThreadExec:
    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor()

    def run(self, funs):
        tasks = [self.executor.submit(fun, args) for fun, args in funs]
        ret = []
        for future in as_completed(tasks):
            try:
                ret.append(future.result())
            except Exception as e:
                ret.append(ThreadExecError(e))
        return ret


def test():
    def util(s):
        time.sleep(s*0.1)
        if s == 2:
            raise Exception("fail")
        return f'finush {s}'
    return ThreadExec().run([(util, i) for i in range(1, 7)])


if __name__ == "__main__":
    print(test())
