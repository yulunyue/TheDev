from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from .cg import World, CgCw
from .model.constant import VE


class Util:
    def get_frames(self):
        return CodingGame(CgCw.name).get_cg_frames()

    def replay(self, c: CodingGame, player_id=0):
        idx = 0
        g = World().set_player_id(player_id)
        for f in self.get_frames():
            idx += 1
            if not f.stderr:
                continue
            if g.maps is None:
                g.load(**f.stderr)
            else:
                g.set_shapes(f.stderr["shapes"])
            state, action = g.get_action()
            c.log(
                f"round:---{idx}----\n{g}\nstate:{VE.to_str(state[0])},{state[1:]};action:{action}"
            )
        return g
