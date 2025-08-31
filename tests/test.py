from .test_ban import TestBan
from app.yly.envs.cg.cart_pole.test import TestCart
from app.yly.envs.cg.cf4.test import C4Test
from app.yly.envs.ml.ciff_walk.test import CfTest
from app.yly.envs.cg.cw.test import CwTest
from app.yly.envs.ml.flv1.test import TestFlv
from app.yly.envs.cg.kululu.test import KululuTest
from app.yly.envs.cg.l9.test import TestL9
from app.yly.envs.cg.mpr.test import MprTest
from .test_mrcf import TestMain
from tests.test_oa import OaTest
from app.yly.envs.cg.pendulum.test import TestPen
from tests.test_tic import TestTicToc
from tests.test_context import LCTest
from common.util.export import logger, random, TestBase, List, File

LOCALS = locals()


class YlyTest:
    def run_random(self):
        fp = File("data/log/yly_run.json")
        record = fp.read_file() if fp.exists() else dict()
        test_has_error: List[TestBase] = []
        tests: List[TestBase] = []
        for k, v in LOCALS.items():
            if k.startswith("_") or getattr(v, "TEST_EMABLE", False) == False:
                continue
            if k == "TestBase":
                continue
            if k not in record:
                record[k] = dict(run_num=0, user_time=0, err_msg="", args="debug")
            if record[k]["err_msg"]:
                test_has_error.append(k)
            else:
                tests.append(k)
        if test_has_error:
            tests = test_has_error
        idx = random.randint(0, len(tests) - 1)
        logger.info(tests[idx])
        instance: TestBase = LOCALS[tests[idx]]()
        r = record[tests[idx]]
        args = r.get("args", "debug")
        r["err_msg"] = instance.run_all_test()
        module_path = str(LOCALS[tests[idx]]).split(" '").pop().split("'")[0]
        module_paths = module_path.split(".")
        module_paths.pop()
        path = ".".join(module_paths)
        logger.info(f"python -m {path} {args}")
        fp.write_file(record)


if __name__ == "__main__":
    YlyTest().run_random()
