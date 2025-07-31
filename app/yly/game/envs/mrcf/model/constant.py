from common.algo.export import np


class Ct:
    MRP_P = [
        [0.9, 0.1, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.5, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.6, 0.0, 0.4],
        [0.0, 0.0, 0.0, 0.0, 0.3, 0.7],
        [0.0, 0.2, 0.3, 0.5, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ]
    MRP_REWARD = [-1, -2, -2, 10, 1, 0]

    def get_cases(self):
        return [
            dict(tp="mrp", method="computer", result=-2.5),
            dict(tp="mdp", method="occu", result="?"),
        ]


C = Ct()
