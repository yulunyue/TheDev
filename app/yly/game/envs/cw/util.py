from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from .cg import World, CgCw
from .model.constant import VE
from common.algo.search.alphabate_search import AlphaBateSearch


class Util:
    ab1 = AlphaBateSearch("ab1").load(1)

    def replay(self, player_id=0):
        idx = 0
        g = World().set_player_id(player_id)
        c = self.get_frames()
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
