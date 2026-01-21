from common.algo.export import ALgoManage, Qlearning
from .ql import Ql


class Al(ALgoManage):
    def gomo885(self):
        from app.yly.envs.game.c5.player.gm_player import GmuMo

        return (
            GmuMo()
            .load("data/tool/C5Tool/best_policy_8_8_5.model", True)
            .set_name("gomo885")
        )

    def gomo664_1500(self):
        from app.yly.envs.game.c5.player.gm_player import GmuMo

        return (
            GmuMo()
            .load(C, "data/tool/C5Tool/best_train_664_1500_policy.model", False)
            .set_name("gomo664_1500")
        )

    def gomo664(self):
        from app.yly.envs.game.c5.player.gm_player import GmuMo

        return (
            GmuMo()
            .load(C, "data/tool/C5Tool/best_policy_6_6_4.model", True)
            .set_name("gomo664")
        )

    def ql(self):
        return Ql().load()
