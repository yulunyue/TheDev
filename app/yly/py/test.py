from common.util.test import TestBase
from .study import Study
class TestPy(TestBase):
    def test_base(self):
        a=Study()
        self.expect(a.a,1)
        self.expect(a.a,2)
        self.expect(getattr(a,'a'),3)
if __name__=="__main__":
    TestPy().run()