from common.util.export import List, Dict
from .shape import ShapeBase, C


class Path:
    def __init__(self):
        self.neutral_shapes: List[ShapeBase] = []
        self.op_shapes: List[ShapeBase] = []
        self.shpae_dis = dict()
        self.op_leader: ShapeBase = None

    def add_shape(self, dis, s: "ShapeBase"):
        if s.unit_type == C.TYPE_CULT_LEADER:
            self.op_leader = s
        elif s.owner == C.OWNER_NEUTRAL:
            self.neutral_shapes.append(s)
        else:
            self.op_shapes.append(s)
        self.shpae_dis[s.k] = dis
