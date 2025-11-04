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


class TestState(AbState):
    idx = 0

    def game_end(self):
        if not self.get_sort_actions():
            return True, self.get_done()
        if self.get_done() is not None:
            return True, self.get_done()
        return False, None

    def get_current_player(self):
        return self.player_id

    @property
    def availables(self):
        return self.get_sort_actions()

    @staticmethod
    def get_new_id():
        TestState.idx += 1
        return TestState.idx

    @staticmethod
    def make_random_state(size=40, min_v=2, max_v=6):
        s = TestState.new().set_player_id(0)
        q = [s]
        while len(q) < size:
            idx = random.randint(0, len(q) - 1)
            cur_state = q.pop(idx)
            states = []
            for i in range(random.randint(min_v, max_v)):
                states.append(TestState.new())
                q.append(states[-1])
            cur_state.set_next_states(states)
        random.shuffle(q)
        for i, v in enumerate(q):
            v.set_reward(i - len(q) // 2)
        return s

    @classmethod
    def new(cls, state=None, **kw):
        if state is None:
            state = TestState.get_new_id()
        return super().new(state, **kw)

    money = 0

    @classmethod
    def make(cls, *states, r=0, player_id=None):
        ret: TestState = cls.new()
        if player_id is not None:
            ret.set_player_id(player_id)
        ret.money = r
        ret.set_next_states(states or [])
        return ret

    def set_next_states(self, states: List["TestState"]):
        return self.set_actions(
            [
                Action(self, i, v.set_player_id(1 - self.player_id))
                for i, v in enumerate(states)
            ]
        )

    @staticmethod
    def make_test_state():
        return TestState.make(
            TestState.make(r=1),
            TestState.make(
                TestState.make(r=2),
                TestState.make(r=-5),
                r=4,
            ),
            TestState.make(
                TestState.make(r=3),
                TestState.make(r=-9),
                TestState.make(r=-3),
                r=-3,
            ),
            player_id=1,
        )

    def show_titles(self):
        if self.game_over:
            return f"r:{self.money}"
        return f"p:{self.player_id}; r:{self.money}"


class Record(ThreadRecord):
    def __init__(self, s: TestState):
        self.s = s
        super().__init__()

    def uk(self):
        return self.s.print_tree()

    def set_search(self, algo: Algo):
        return self.set_exec(lambda *args: algo.search(self.s))


def get_s(cls=None, **kw):
    if cls is not None:
        md = Module().load_module_object(cls)
        md.reset_env(**kw)
        return md.new(**kw)
    else:
        return TestState.make_test_state()


class SearchTool(ToolBase):
    def prepare(self, **kw):
        self.al = ALgoManage().set_record_dir("data/test/search")

    def mc_cli(self):
        Record(self.s).set_search(self.al.mc()).cli()

    def mc(self, cls=None):
        s = get_s(cls)
        self.al.mc().search(s)

    def ql(self):
        algo = self.al.ql()
        algo.train(self.s)
        logger.debug(algo.show())

    def debug(self):
        self.mc("app.yly.envs.game.c5.state.State")


if __name__ == "__main__":
    random_seed(7)
    SearchTool().run()
