from common.tool.thread_util import run_watch_fun
from common.service.http import Node
from common.util.module import Module
from common.util.log import logger
import os


class SolutionBase:
    logs = ""

    def get_cases(self):
        return [

        ]

    def execute(self):
        RECORD_ENABLE = True

    @classmethod
    def log(cls, *s, tp: str = ""):
        if len(cls.logs) >= 102400:
            return
        if tp:
            cls.draw(s[0], tp)
        cls.logs += " ".join([str(v) for v in s])+"\n"

    @classmethod
    def draw(cls, s, tp: str):
        from common.third_util.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):

        for case in self.get_cases():
            self.__class__.logs = ""
            self.ep = case.pop("result")
            if 'info' in case:
                case.pop('info')
            try:
                r = self.execute(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                print(case, 'result', r, 'except', self.ep)
                print(self.__class__.logs)
                break

    @classmethod
    def cls_run(cls):

        for case in cls.get_cases():
            cls.logs = ""
            m, inp, es = case
            r = cls(*inp[0])
            cls.log(m[0], *inp[0])
            flag = True
            for i in range(1, len(inp)):
                cls.log(m[i], inp[i], es[i])
                try:
                    e = getattr(r, m[i])(*inp[i])
                except Exception as a:
                    e = a
                if not r.diff(e, es[i]):
                    print(f'{cls.logs}, result:{e}, expect:{es[i]}')
                    flag = False
                    break
            if not flag:
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
