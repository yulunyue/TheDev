from common.util.export import List, Dict
from .shape import ShapeBase, C


class Path:
    def __init__(self):
        self.shapes: List[List[ShapeBase]] = [[], [], []]
        self.shpae_dis: Dict[str, int] = {}
        self.leaders: List[ShapeBase] = [None, None]

    def add_shape(self, dis, s: "ShapeBase"):
        if s.unit_type == C.TYPE_CULT_LEADER:
            self.leaders[s.owner] = s
        else:
            self.shapes[s.owner].append(s)
        # self.shpae_dis[s.k] = dis

    def get_near(self, player_id: int):
        a = self.shapes[player_id]
        return a[0] if a else None
