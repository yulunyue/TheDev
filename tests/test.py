from .test_ban import TestBan
from .test_cart import TestCart
from tests.test_cf4 import C4Test
from tests.test_cf import CfTest
from tests.test_cw import CwTest
from app.yly.envs.ml.flv1.test import TestFlv
from tests.test_lulu import KululuTest
from tests.test_l9 import TestL9
from tests.test_mpr import MprTest
from .test_mrcf import TestMain
from tests.test_oa import OaTest
from tests.test_pdl import TestPen
from tests.test_tic import TestTicToc
from tests.test_context import LCTest
from common.util.export import logger, random, TestBase, List, File
from common.tool.export import TableConfig, TableBase, StrModel, DictModel

LOCALS = locals()


class RunModel(TableConfig):
    calls = DictModel()


class YlyTest:
    def __init__(self):
        self.tb = TableBase[RunModel]().set_resource("yly_random_run")
        for k, v in LOCALS.items():
            if isinstance(v, TestBase):
                self.tb.insert(k, calls=dict(run_all_test=""))

    def run_random(self):
        calls = []
        for t in self.tb.all():
            s = LOCALS[t.key]()
            for k, v in t.calls.get_value().items():
                calls.append([s, k, v])
        s, k, v = calls[random.randint(0, len(calls)) - 1]
        args = [u for u in v.split("#")[0].split(",") if u]
        getattr(s, k)(*args)


if __name__ == "__main__":
    YlyTest().run_random()
