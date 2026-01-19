import numpy as np
from common.util.export import MockCf


def GeLU(x: np.ndarray):
    pass


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                x=np.array([-2.0, -1.0, 0.0, 1.0, 2.0]),
                result=[-0.0454, -0.1588, 0.0, 0.8412, 1.9546],
            )
        )

    def execute(self, x):
        return GeLU(x)


if __name__ == "__main__":
    Solution().run()
