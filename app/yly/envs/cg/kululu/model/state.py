from common.algo.search.state import State
from .grid import Grid
from common.util.export import List


class KuState(State):
    g: Grid

    @staticmethod
    def set_env(s: str, params):
        KuState.g = Grid().load_map(s)

    def to_str(self):
        board_row: List[List[str]] = []
        for i, row in enumerate(KuState.g.borads):
            board_row.append([])
            for j, c in enumerate(row):
                board_row[-1].append(c.view())

        for p in KuState.g.nodes_list:
            board_row[p.y][p.x] = p.view()
        for a in self.get_actions().values():
            board_row.append(str(a))
        return "\n".join(["".join(rows) for rows in board_row])
