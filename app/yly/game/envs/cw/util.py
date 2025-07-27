from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from .cg import World


class Util:

    def replay(self, c: CodingGame, aim_id=None, player_id=0):
        idx = 0
        g = World().set_player_id(player_id)
        for f in c.get_cg_frames():
            idx += 1
            if not f.stderr:
                continue
            if g.maps is None:
                g.load(**f.stderr)
            else:
                g.set_shapes(f.stderr["shapes"])
            if aim_id is not None:
                if idx >= aim_id and aim_id != -1:
                    return g
            else:
                dst = g.get_action()
                c.log(f"round:---{idx}----\n{g}\naction:{dst}")
        return g
