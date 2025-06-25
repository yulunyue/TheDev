from common.util.export import TestBase, Module, logger, SolotionBase


class LCTest(TestBase):
    uri = "https://leetcode.cn"

    def test_run(self, name, fun_name):
        md = Module().load_module(f"app.yly.algo.lc.{name}")
        Module().compile_one(f"app/yly/algo/lc/{name}.py")
        ins: SolotionBase = md.Solution()
        logger.enable_cache()
        for c in ins.get_cases():
            s = c.pop("result") if "result" in c else None
            try:
                r = getattr(ins, fun_name)(**c)
            except Exception as e:
                r = str(e)
            self.expect(r, s, "\n" + logger.get_and_clear_cache())


if __name__ == "__main__":
    LCTest().run()
