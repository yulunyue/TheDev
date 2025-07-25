from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from .cg import World


class Util:

    def replay(self, c: CodingGame):
        idx = 0
        g = World()
        for f in c.get_cg_frames():
            idx += 1
            if not f.stderr:
                continue
            if g.maps is None:
                g.load(**f.stderr)
            else:
                g.set_shapes(f.stderr["shapes"])
            dst = g.get_action()
            c.log(f"round:---{idx}----\n{g}\naction:{dst}")
