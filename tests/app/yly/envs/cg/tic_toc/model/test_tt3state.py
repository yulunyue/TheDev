from common.util.export import TestBase
from app.yly.envs.cg.tic_toc.model.ttstate3 import TtState3


class Tt3Test(TestBase):
    @classmethod
    def setup_class(cls):
        cls.s = TtState3.new()
        return super().setup_class()
