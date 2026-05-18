from .task_base import ZbTask, File, OsUtil, Module, logger, CS
from common.third_service.git_tool.git_util import GitUtil
from common.model.git.patch import Patch


class SelfTask(ZbTask):

    def py_test(self, key) -> dict:
        f = Module().load_module_object(
            "run_verification.run_py_test", self.input_dir.path
        )
        # result=self.local_cfg.result.get_value()
        statu_code, msg, msg1, ct, result, *args = f(key)
        self.input_dir.child(f"{key}.log").write_file(msg)
        self.logger.debug(f"statu_code={statu_code}\nmsg1={msg1}\nresult={result}")
        result_json_file = self.local_repo.child(CS.RESULT_JSON_FILE)
        if result_json_file.exists():
            result_json_file.copy_to(
                self.input_dir.child(f"{key}.json"), over_write=True
            )
        File(f"{key}.json").remove()

    def pip(self):
        File(self.venv_dir).remove()
        OsUtil("bash").run(self.setup_env_sh.get_abs_path())

    def play(self):
        self.apply_test()
        self.py_test("test")
        self.apply_code()
        self.py_test("code")
        self.print_result()

    def run0(self):
        self.rest_repo()
        self.py_test("pre")

    def run1(self):
        self.apply_test()
        self.py_test("test")

    def run2(self, **kw):
        self.apply_code()
        self.py_test("code")
