from common.util.export import ToolBase, logger, log, time, File
from common.algo.export import ALgoManage, random_seed, Algo
from app.yly.envs.game.c5.state import State, C
from app.yly.envs.game.c5.constant import load


class Al(ALgoManage):
    def gomo885(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        return GmuMo().load(C, "data/tool/C5Tool/best_policy_8_8_5.model", True)


class C5Tool(ToolBase):
    def prepare(self, env: str):
        load(*[int(v) for v in env.split("_")])
        self.s = State.new(C.state)
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
        logger.info(self.al.actor(names.split(","))[-1])

    def fight(self, names="", turn=1):
        self.al.set_players(names.split(",")).fight(int(turn))

    def dev(self):
        pass

    def debug(self):
        self.train_mumo()


if __name__ == "__main__":
    random_seed(4)
    C5Tool().run()
