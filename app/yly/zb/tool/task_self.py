from .task_base import ZbTask, File, OsUtil, Module, logger
from common.third_service.git_tool.git_util import GitUtil, Patch


class SelfTask(ZbTask):

    def py_test(self, key) -> dict:
        f = Module().load_module_object(
            "run_verification.run_py_test", self.input_dir.path
        )
        statu_code, msg, msg1, ct, result = f(key)
        self.logger.debug(
            f"statu_code={statu_code}\nstdout={msg}\nstderr={msg1}\nresult={result}"
        )
        logger.info(f"{key}:{ct}")

    def play(self):
        if not File(self.venv_dir).exists():
            OsUtil("python").set_venv(self.venv_dir)
            OsUtil("bash").run(self.setup_env_sh.get_abs_path())
        self.run1()
        self.run2()
        self.print_result()

    def run0(self):
        self.rest_repo()
        self.py_test("pre")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.py_test("test")

    def run2(self, **kw):

        self.py_test("code")
