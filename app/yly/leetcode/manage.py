from common.tool.thread_util import run_watch_fun
from common.service.http import Node
from common.util.module import Module
from common.util.log import logger
import os


class SolutionBase:
    def get_cases(self):
        return [

        ]

    def execute(self):
        RECORD_ENABLE = True

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, "execute")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 102400:
            return
        if tp:
            self.draw(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        from common.third_util.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):

        for case in self.get_cases():
            self.logs = ""
            self.ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                print(case, 'result', r, 'except', self.ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


PATH = 'app/yly/leetcode/view'


class Route:

    def query(self, path=PATH):
        ret = Node(value=path)
        for name in os.listdir(path):
            if not name.endswith('.py'):
                continue
            moudle_name = path.replace('/', '.')+"."+name.replace('.py', '')
            f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
            ret.add_child(value=moudle_name, data=f.get_cases())
        return ret

    def execute(self, moudle_name, case):
        f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
        return Node(data=run_watch_fun(f.execute, **case)).to_json()


def test():
    r = Route()
    info = r.query().childs[0]
    r.execute(info.value, info.data[0])


if __name__ == "__main__":
    test()
