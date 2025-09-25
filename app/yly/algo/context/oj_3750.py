from common.util.export import List, Dict, logger
from common.mock import MockCf

O1 = """Case:1
000:00 red iceman 1 born
000:00 blue lion 1 born
000:10 red iceman 1 marched to city 1 with 50 elements and force 50
000:10 blue lion 1 marched to city 2 with 50 elements and force 50
000:30 red iceman 1 earned 10 elements for his headquarter
000:30 blue lion 1 earned 10 elements for his headquarter
000:50 59 elements in red headquarter
000:50 59 elements in blue headquarter
001:00 red lion 2 born
001:00 blue dragon 2 born
001:10 red lion 2 marched to city 1 with 50 elements and force 50
001:10 blue lion 1 marched to city 1 with 50 elements and force 50
001:10 red iceman 1 marched to city 2 with 41 elements and force 70
001:10 blue dragon 2 marched to city 2 with 10 elements and force 20
001:40 red lion 2 attacked blue lion 1 in city 1 with 50 elements and force 50
001:40 blue lion 1 was killed in city 1
001:40 red lion 2 earned 10 elements for his headquarter
001:40 blue dragon 2 attacked red iceman 1 in city 2 with 10 elements and force 20
001:40 red iceman 1 fought back against blue dragon 2 in city 2
001:40 blue dragon 2 was killed in city 2
001:40 red iceman 1 earned 10 elements for his headquarter
001:50 21 elements in red headquarter
001:50 49 elements in blue headquarter
002:00 blue ninja 3 born
002:10 red lion 2 marched to city 2 with 100 elements and force 50
002:10 blue ninja 3 marched to city 2 with 20 elements and force 50
002:10 red iceman 1 reached blue headquarter with 29 elements and force 70
002:40 blue ninja 3 attacked red lion 2 in city 2 with 20 elements and force 50
002:40 red lion 2 fought back against blue ninja 3 in city 2
002:40 blue ninja 3 was killed in city 2
002:40 red lion 2 earned 10 elements for his headquarter
002:40 red flag raised in city 2
002:50 23 elements in red headquarter
002:50 29 elements in blue headquarter
003:10 red lion 2 reached blue headquarter with 58 elements and force 50
003:10 blue headquarter was taken"""
O2 = """Case:2
000:00 red iceman 1 born
000:00 blue lion 1 born
000:10 red iceman 1 marched to city 1 with 20 elements and force 20
000:10 blue lion 1 marched to city 1 with 20 elements and force 20
000:40 red iceman 1 attacked blue lion 1 in city 1 with 20 elements and force 20
000:40 blue lion 1 was killed in city 1
000:40 red iceman 1 earned 10 elements for his headquarter
000:50 22 elements in red headquarter
000:50 20 elements in blue headquarter
001:00 red lion 2 born
001:00 blue dragon 2 born
001:10 red lion 2 marched to city 1 with 20 elements and force 20
001:10 blue dragon 2 marched to city 1 with 20 elements and force 20
001:10 red iceman 1 reached blue headquarter with 39 elements and force 40
001:40 red lion 2 attacked blue dragon 2 in city 1 with 20 elements and force 20
001:40 blue dragon 2 was killed in city 1
001:40 red lion 2 earned 10 elements for his headquarter
001:40 red flag raised in city 1
001:50 12 elements in red headquarter
001:50 0 elements in blue headquarter
002:10 red lion 2 reached blue headquarter with 20 elements and force 20
002:10 blue headquarter was taken"""


class Action:
    pass


LOGS: Dict[int, List[Action]] = dict()


class Unit:
    attack_power: int = None
    init_hp: int = None


class Dragon(Unit):
    pass


class Ninja(Unit):
    pass


class IceMan(Unit):
    pass


class Lion(Unit):
    pass


class Wolf(Unit):
    pass


SHAPES: List[Unit] = [Dragon, Ninja, IceMan, Lion, Wolf]


class Commander:
    RED = 1
    BLUE = 0

    def __init__(self, key, hp):
        self.hp = hp
        self.key = key
        if key == Commander.RED:
            self.shape_clss: List[Unit] = [IceMan, Lion, Wolf, Ninja, Dragon]
        else:
            self.shape_clss: List[Unit] = [Lion, Ninja, Dragon, IceMan, Wolf]


class Solution(MockCf):
    def get_cases(self):
        return [
            dict(
                main_hp=99,
                city_num=2,
                t=1000,
                init_hps=[10, 20, 50, 50, 30],
                init_attack_power=[20, 50, 50, 50, 50],
                case_id=1,
                result=O1,
            ),
            # dict(
            #     main_hp=40,
            #     city_num=1,
            #     t=1000,
            #     init_hps=[20, 20, 20, 20, 20],
            #     init_attack_power=[20, 20, 20, 20, 20],
            #     result=O2,
            # ),
        ]

    def execute(self, main_hp, city_num, t, init_hps, init_attack_power, case_id):
        self.main_hps = [
            Commander(Commander.RED, main_hp),
            Commander(Commander.BLUE, main_hp),
        ]
        self.city_num, self.max_t = city_num, t
        for i, v in enumerate(SHAPES):
            v.attack_power, v.init_hp = init_attack_power[i], init_hps[i]
        LOGS.clear()
        self.t = 0
        while self.t < self.max_t:
            tm = self.t % 60
            if getattr(self, f"do_when_{tm}")():
                break
            self.t += 10
        ans = [f"Case:{case_id}"]
        for t in sorted(LOGS.keys()):
            k = "%03d:%d" % (t // 60, t % 60)
            for a in LOGS[t]:
                ans.append(f"{k} {a}")
        return "\n".join(ans)

    def do_when_0(self):
        pass

    def do_when_10(self):
        pass

    def do_when_20(self):
        pass

    def do_when_30(self):
        pass

    def do_when_40(self):
        pass

    def do_when_50(self):
        pass

    def main(self):
        cases, *args = self.ii()
        for i in range(cases):
            main_hp, city_num, t = self.ii()
            init_hps = self.ii()
            init_attack_power = self.ii()
            print(
                self.execute(main_hp, city_num, t, init_hps, init_attack_power, i + 1)
            )


if __name__ == "__main__":
    Solution().main()
