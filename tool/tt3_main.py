from app.yly.envs.cg.tic_toc.model.ttstate3 import TtState3
from common.util.export import ToolBase
from common.algo.export import ALgoManage


class Tt3Tool(ToolBase):
    def prepare(self, *args):
        self.s = TtState3.new(0)
        self.al = ALgoManage().set_state(self.s)
        return super().prepare(*args)

    def actor(self, names: str):
        self.al.actor(names.split(","))

    def fight(self, names: str, turn=1) -> None:
        self.al.set_players(names.split(",")).fight(int(turn))


if __name__ == "__main__":
    Tt3Tool().run()
