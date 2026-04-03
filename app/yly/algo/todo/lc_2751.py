from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                positions=[5, 4, 3, 2, 1],
                healths=[2, 17, 9, 15, 10],
                directions="RRRRR",
                result=[2, 17, 9, 15, 10],
            )
        )

    def survivedRobotsHealths(
        self, positions: List[int], healths: List[int], directions: str
    ) -> List[int]:
        """
        在一条线上有n个机器人,每个机器人有一个生命值,前进的方向
        每个机器人同时以相同的速度朝给定的方向启动，
        当发生碰撞时,生命值较小的机器人会消失,较大的机器人生命值会减少一
        求最终状态机器人的生命值
        """
        n = len(positions)
        phd = sorted([[positions[i], healths[i], directions[i], i] for i in range(n)])
        self.logger.map(phd=phd)
        s = []
        for p, h, d, i in phd:
            fg = True
            while s and s[-1] == "R" and d == "L":
                fg = False
                lp, lh, ld, j = s.pop()
                if lh == h:
                    break
                if lh < h:
                    h -= 1
                if lh > h:
                    s.append([lp, lh - 1, ld, j])
                    break
            if fg:
                s.append([p, h, d, i])
            self.log(s=s)
        ret = [None] * n
        for u in s:
            ret[u[-1]] = u[1]
        return [v for v in ret if v is not None]

    execute = survivedRobotsHealths
