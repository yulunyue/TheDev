from common.util.export import get_log, uid, THE_DEV_CONSTANT, List, Dict
from common.service.node import Node
from .bp_record import BpRecord, logger


class BpNode:
    key = None
    state = THE_DEV_CONSTANT.STATE_WAIT

    def __init__(self):
        self.value = None
        self.childs: Dict[str, BpNode] = dict()
        self.record: BpRecord = None

    def set_value(self, value):
        self.value = value
        return self

    def get_value(self):
        self.record.record("get_value", self)
        return self.value

    def view(self):
        ret = Node(value=THE_DEV_CONSTANT.FlowChartTD)

        def util(n: BpNode):
            ret.data[n.key] = dict(value=n.get_value())

        self.bfs(util)
        return ret

    def bfs(self, util):
        vt = set()
        q = [self]
        while q:
            t = q
            q = []
            for s in t:
                util(s)
                for c in s.childs.values():
                    if c.key in vt:
                        continue
                    vt.add(c.key)
                    q.append(c)

    def init_env(self):
        record = BpRecord()

        def util(v: BpNode):
            # logger.debug(f"init_env {v}")
            v.record = record

        self.bfs(util)

    def __repr__(self):
        return f"name:{self.key} childs:{len(self.childs)} value:{self.get_value()}"
