from common.mock import CgMock
from app.yly.game.envs.cf4.model.constant import C
from app.yly.game.envs.cf4.model.cf4state import F4State
from common.util.export import logger


class CgSolve(CgMock):
    game_id = "70989184688f3ec2cf6e1e24a36c1ea631ab8523"

    def excecute(self, su):
        ret = ["NONE", "NONE"]
        k = C.any_to_mask(su, 0)
        s = F4State.new_state(k)
        for i in range(2):
            for a in s.get_player_actions(i).values():
                # logger.info(a.dst)
                if a.dst.get_done() != i:
                    continue
                if ret[i] == "NONE":
                    ret[i] = str(a.action)
                else:
                    ret[i] += f" {a.action}"

        return "\n".join(ret), s

    def run(self):
        s = "\n"
        for _ in range(6):
            s += self.input() + "\n"
        self.debug()
        print(self.excecute(s)[0])


if __name__ == "__main__":
    CgSolve().run()
