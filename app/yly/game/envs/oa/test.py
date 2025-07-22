from common.util.export import TestBase, logger, Module
from common.third_util.export import CodingGame
from common.algo.export import AlphaBateSearch, ALgoManage
from app.yly.game.envs.oa.cg import CgOa, Rooms, C


class CwTest(TestBase):
    def test_pk(self):
        Module().compile_one("app/yly/game/envs/oa/cg.py")
        CodingGame(CgOa.name).pk(Module.RUN_TMP_PATH, CgOa.game_id, CgOa.agentsIds)

    def test_base(self):
        r = Rooms.new(C.INIT_MASK).get_action(2).dst

        # a = AlphaBateSearch().search(r)
        logger.info(r)

    def test_replay(self):
        s = Rooms.new(C.INIT_MASK)
        for a in CodingGame(CgOa.name).get_replay_json():
            if not a.stdout:
                break
            s = s.get_action(int(a.stdout)).dst
            logger.info(s)


if __name__ == "__main__":
    CwTest().run()
