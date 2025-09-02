from common.util.export import List, ii, defaultdict, logger
from app.yly.envs.cg.mpr.cg import Mpr, C
from common.third_util.export import EChart, Draw
from common.third_service.export import CGFrames, CodingGame
from .model.data import Data


class Util(CodingGame):

    def show(self):
        history: List[Data] = []
        for i, f in enumerate(self.get_cg_frames()):
            if not f.stderr:
                continue
            Data().set_history(history).set_data(**f.stderr)
        datas = [d.dump() for d in history]
        self.get_local_file("record.json").write_file(datas)
        EChart().draw_lines(datas, gui1=False).save(
            self.get_local_file(f"record.html").path
        )
