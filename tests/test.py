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


class YlyTest:
    def run(self):
        pass


if __name__ == "__main__":
    YlyTest().run()
