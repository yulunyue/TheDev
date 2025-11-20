from common.util.export import ToolBase, logger, Module, random, List
from common.algo.export import (
    AbState,
    AbDev,
    Algo,
    Action,
    State,
    MctsSearch,
    ALgoManage,
    random_seed,
)
from common.tool.export import ThreadRecord
from app.yly.envs.game.study.state import TestState


def get_s(cls=None, **kw):
    md = Module().load_module_object(cls)
    return md.get_root(**kw)


DEFAULT_CLS = 1


class SearchTool(ToolBase):
    def prepare(self):
        self.al = ALgoManage().set_record_dir("data/test/search")

    def mc_cli(self):
        Record(self.s).set_search(self.al.mc()).cli()

    def mc(self, cls=None):
        s = TestState
        self.al.mc().search(s)

    def ql(self, cls=""):
        s: State = get_s(cls)
        logger.debug(s.print_tree())
        algo = self.al.ql()
        algo.train(s)
        logger.debug(algo.show())

    def dev(self):
        pass


if __name__ == "__main__":
    random_seed(7)
    SearchTool().run()
