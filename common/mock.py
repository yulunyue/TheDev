import json
import sys
import bisect
import functools


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log


class CgMock:
    inputs = []

    def input(self):
        ret = input()
        self.inputs.append(ret)
        return ret

    def debug(self, **kw):
        ans = dict(inputs=self.inputs)
        ans.update(kw)
        print(json.dumps(ans), file=sys.stderr)
        self.inputs.clear()
