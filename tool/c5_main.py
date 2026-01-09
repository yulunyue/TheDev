from common.util.export import ToolBase, logger, log, time, File
from common.algo.export import ALgoManage, random_seed, Algo
from app.yly.envs.game.c5.state import State


class Al(ALgoManage):
    def gomo885(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        return (
            GmuMo()
            .load("data/tool/C5Tool/best_policy_8_8_5.model", True)
            .set_name("gomo885")
        )

    def gomo664_1500(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        return (
            GmuMo()
            .load(C, "data/tool/C5Tool/best_train_664_1500_policy.model", False)
            .set_name("gomo664_1500")
        )

    def gomo664(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        return (
            GmuMo()
            .load(C, "data/tool/C5Tool/best_policy_6_6_4.model", True)
            .set_name("gomo664")
        )


class C5Tool(ToolBase):
    def prepare(self, env: str):
        State.set_board(*[int(v) for v in env.split("_")])
        self.s = State.new(State.C.state)
        self.al = Al().set_state(self.s)
        return self

    def do_cmd(self, method, *args):
        try:
            if method == "put":
                pos = int(args[0]) * C.width + int(args[1])
                self.s = self.s.get_action(pos).get_dst()
            self.info(f"{method} {args}")
            self.info(self.s.show())
        except Exception as e:
            self.info(f"{method} {args} {e}")
            self.info(self.s.show())

    def actor(self, names=""):
        self.al.actor(names.split(","))

    def fight(self, names="", turn=1):
        self.al.set_players(names.split(",")).fight(int(turn))

    def train(self, name):
        self.al.get_player(name).train(self.s)

    def dev(self):
        pass

    def debug(self):
        self.train("gomo664_1500")


if __name__ == "__main__":
    random_seed(4)
    C5Tool().run()
