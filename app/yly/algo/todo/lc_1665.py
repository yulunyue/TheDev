from common.util.export import List, Dict, functools, CT, LOG


class Solution:
    """
    0 消耗
    1 启动需要最少
    """

    def minimumEffort(self, tasks: List[List[int]]) -> int:
        t = sorted([[v[0], v[1]] for i, v in enumerate(tasks)])
