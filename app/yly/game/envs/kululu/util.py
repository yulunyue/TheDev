from common.third_util.export import CGFrames
from common.util.export import List, File
from app.yly.game.envs.kululu.cg import Kululu, Grid


class Util:

    def replay(self, frames: List[CGFrames]):
        idx = 0
        g = Grid()
        for f in frames:
            idx += 1
            if not f.stderr:
                continue
            g.load_from_json(**f.stderr)
            dst = g.get_action()
            self.log(f"round:---{idx}----\n{g}\naction:{dst}")

    _log = None

    def log(self, msg):
        if self._log is None:
            self._log = File(f"{Kululu.tmp_dir()}/replay.log").get_writer()
        self._log.write(f"{msg}\n")
        self._log.flush()
