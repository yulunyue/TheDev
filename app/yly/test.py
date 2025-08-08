from app.yly.game.envs.bandit.test import TestBan
from app.yly.game.envs.cart_pole.test import TestCart
from app.yly.game.envs.cf4.test import C4Test
from app.yly.game.envs.ciff_walk.test import CfTest
from app.yly.game.envs.cw.test import CwTest
from app.yly.game.envs.flv1.test import TestFlv
from app.yly.game.envs.kululu.test import KululuTest
from app.yly.game.envs.l9.test import TestL9
from app.yly.game.envs.mpr.test import MprTest
from app.yly.game.envs.mrcf.test import TestMain
from app.yly.game.envs.oa.test import OaTest
from app.yly.game.envs.pendulum.test import TestPen
from app.yly.game.envs.tic_toc.test import TestTicToc
from app.yly.algo.context.test import LCTest
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
        r["err_msg"] = ""
        args = r.get("args", "debug")
        try:
            instance.run_all_test()
            r["run_num"] += 1
        except Exception as e:
            r["err_msg"] = str(e)
            raise Exception(instance, e)
        finally:
            module_path = str(LOCALS[tests[idx]]).split(" '").pop().split("'")[0]
            module_paths = module_path.split(".")
            module_paths.pop()
            path = ".".join(module_paths)
            logger.info(f"python3 -m {path} {args}")
            fp.write_file(record)


if __name__ == "__main__":
    YlyTest().run_random()
