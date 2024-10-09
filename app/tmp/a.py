from typing import List, Dict, Optional
from functools import lru_cache


class Solution:
    def escapeMaze(self, maze: List[List[str]]) -> bool:
        k, m, n = len(maze), len(maze[0]), len(maze[0][0])
        # vis =[[[[False] * 6 for _ in range(n)] for _ in range(m)] for _ in range(k)]
        # s 的最低位：是否使用了临时消失术
        # s 的其余位：0-未使用永久消除术，1-当前正位于永久消除的位置，2-已使用永久消除术

        @lru_cache(None)
        def dfs(t, x, y, s):
            if x < 0 or x >= m or y < 0 or y >= n or t + m - 1 - x + n - 1 - y >= k:
                return False
            if x == m - 1 and y == n - 1:
                return True
            if s >> 1 == 1:
                for nx, ny in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
                    if dfs(t + 1, nx, ny, s ^ 6):  # 跳出永久消除的位置
                        return True
                return dfs(t + 1, x, y, s)
            # 尝试使用永久消除术
            if s >> 1 == 0 and maze[t][x][y] == '#' and dfs(t, x, y, s | 2):
                return True
            # 使用永久消除术已无法走到终点，遇到障碍只能使用临时消除术
            if maze[t][x][y] == '#':
                if s & 1 == 1:
                    return False
                s |= 1
            for nx, ny in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
                if dfs(t + 1, nx, ny, s):
                    return True
            return dfs(t + 1, x, y, s)

        return dfs(0, 0, 0, 0)
