from common.util.test import TestBase
from common.algo.util import *
import math
class TestAlgo(TestBase):
    def test_graph(self):
        pass

    def test_util(self):
        self.expect(sin(90),1)
        self.expect(cos(180),-1)
        for i in range(0,361,45):
            self.expect(int(calc_angle(
                0,0,3*sin(i),3*cos(i)
            )/math.pi*180),i,i)
        self.expect(
            list(combinations([1,2,3],2)),
            [(1,2),(1,3),(2,3)]
        )
        self.expect(
            list(permutations([1,2,3],2)),
            [(1,2),(1,3),(2,3)]
        )
    def test_math(self):
        self.expect(math.gcd(12),[])
if __name__=="__main__":
    TestAlgo().run()