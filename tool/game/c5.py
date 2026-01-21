from common.util.export import logger, log, time, File
from common.tool.export import ToolBase
from common.algo.export import ALgoManage, random_seed, Algo, Qlearning
from app.yly.envs.game.c5.model.dyn_state import StateStatic, DynState
from app.yly.envs.game.c5.player.al import Al


class C5Tool(ToolBase):
    def prepare(self, env: str, tp, s: str = None):
        clss = dict(dyn=DynState, sst=StateStatic)[tp]
        random_seed(1)
        self.s = clss.set_board(*[int(v) for v in env.split("_")], state=s)
        self.al = Al().set_state(self.s)
        return self

    # def do_cmd(self, method, *args):
    #     try:
    #         if method == "put":
    #             pos = int(args[0]) * C.width + int(args[1])
    #             self.s = self.s.get_action(pos).get_dst()
    #         self.info(f"{method} {args}")
    #         self.info(self.s.show())
    #     except Exception as e:
    #         self.info(f"{method} {args} {e}")
    #         self.info(self.s.show())

    def actor(self, env, tp, names):
        self.prepare(env, tp)
        self.al.actor(names.split(","))

    def fight(self, env, tp, names, turn):
        self.prepare(env, tp)
        self.al.set_players(names.split(",")).fight(int(turn))

    def train(self, env, tp, name, s="", **kw):
        self.prepare(env, tp, s)
        self.al.get_player(name).set_options(**kw).train(self.s)


if __name__ == "__main__":
    C5Tool().run()
