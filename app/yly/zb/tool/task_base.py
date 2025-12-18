from common.util.export import (
    ToolBase,
    File,
    logger,
    Dict,
    List,
    StrUtil,
    Module,
    get_log,
    sys,
)
from common.tool.export import (
    OsUtil,
)
from common.third_service.git_tool.git_util import GitUtil, Patch
from ..model.export import (
    INPUTS_DIR,
    INFO_DIR,
    REPO_BASE,
    Cg,
    task_cfg,
    TaskCfg,
    get_info_by_name,
    TASK_DIR,
    CS,
    get_result,
    REPO_DIR,
)


import os


class ZbTask:
    @property
    def logger(self):
        return get_log(f"zb/{self.repo}/{self.task_id}_{self.pr.number}")

    def build(self, local_cfg):
        self.local_cfg: TaskCfg = local_cfg
        if not self.local_cfg.resource.exists():
            raise Exception(f"{self.local_cfg.resource} not exist")
        self.name, self.task_id = self.local_cfg.name.get_value(), self.local_cfg.key
        self.input_dir = self.local_cfg.input_dir
        if not self.input_dir.exists():
            raise Exception(self.input_dir.path, "not exist")
        self.cfg: Cg = self.local_cfg.cg
        self.owner, _, self.repo, self.pr_numer = get_info_by_name(
            self.local_cfg.name.get_value()
        )
        logger.info(self.local_cfg.resource)
        logger.info(self.cfg.resource)
        self.zip_file = self.input_dir.child(self.local_cfg.name.get_value() + ".zip")
        self.local_cfg.pr_url.set_value(self.cfg.pr_url.get_value())
        self.local_cfg.issue_url.set_value(self.cfg.issue_url.get_value())
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.git_cmd = self.cfg.get_git_util()
        self.local_repo = self.git_cmd.local_dir
        self.pr = self.git_cmd.get_pr(self.pr_numer)
        self.setup_env_sh = self.input_dir.child("setup_env.sh")
        self.test_patch = self.pr.get_patch(self.input_dir.child("test.patch"))
        self.code_patch = self.pr.get_patch(self.input_dir.child("code.patch"))
        test_main_values = self.local_cfg.test_main.get_value()
        if not test_main_values:
            self.change_py_test_files: Dict[str, File] = dict()
            self.get_update_file_by_batch(self.test_patch)
            self.get_update_file_by_batch(self.code_patch)
            files = list(self.change_py_test_files.keys())
            self.local_cfg.test_main.set_value(files)
        if isinstance(test_main_values, str):
            self.local_cfg.test_main.set_value(test_main_values.split(" "))
        return self

    def apply_patch(self, f: Patch):
        self.git_cmd.apply(f.f.get_abs_path())

    def apply_code(self):
        self.apply_test()
        self.apply_patch(self.code_patch)

    def apply_test(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)

    def get_update_file_by_batch(self, fp: Patch):
        files = []
        for f in fp.get_change_files():
            if f.local.file_name.endswith(".py") and f.local.file_name.startswith(
                "test_"
            ):
                key = f.filename
                if key not in self.change_py_test_files:
                    self.change_py_test_files[key] = f
                    files.append(f.local.path)
        logger.info(f"{fp.f} - {' '.join(files)[:100]}")

    def make_setup_repo_sh(self):
        self.input_dir.child("setup_repo.sh").write_file(
            "\n".join(
                [
                    "set -e",
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git config --global http.sslVerify false",
                    f"git clone {self.git_cmd.repo} {self.local_repo.path}",
                ]
            )
        )

    def re_init(self):
        self.input_dir.remove()
        File(self.input_dir.path + ".zip").unzip()
        self.init()

    def finish(self, statu, msgs):

        self.local_cfg.error_msg.set_value(msgs)
        if statu:
            logger.info(f"ZB_TASK_SUCCESS {self.task_id} {self.zip_file} {msgs}")
            self.local_cfg.zip()
            self.save()
        else:
            msg = f"{CS.ZB_TASK_FAIL} {self.task_id} {self.zip_file} {msgs}"
            logger.info(msg)
            self.zip_file.remove()
            self.save()
            raise Exception(msg)

    def print_result(self):
        local_result: dict = self.local_cfg.result.get_value()
        local_result.clear()
        old, old_ct = get_result(self.input_dir.child("test.json").path)
        logger.info(f"test:{old_ct}")
        new, new_ct = get_result(self.input_dir.child("code.json").path)
        logger.info(f"code:{new_ct}")
        local_result["test"], local_result["code"] = old, new
        fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass = [], [], [], []

        for k in set(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                if new_statu == CS.PASSED:
                    fail_to_pass.append(k)
                elif old_statu == CS.PASSED:
                    pass_to_fail.append(k)
            elif old_statu == new_statu:
                if new_statu == CS.PASSED:
                    pass_to_pass.append(k)
                elif new_statu == CS.FAILED:
                    fail_to_fail.append(k)
        local_result[CS.FAIL_TO_FAIL] = sorted(fail_to_fail)
        local_result[CS.PASS_TO_FAIL] = sorted(pass_to_fail)
        local_result[CS.FAIL_TO_PASS] = sorted(fail_to_pass)
        local_result[CS.PASS_TO_PASS] = sorted(pass_to_pass)
        self.cfg.PASS_TO_PASS.set_value(pass_to_pass)
        self.cfg.FAIL_TO_PASS.set_value(fail_to_pass)
        if fail_to_fail:
            self.finish(False, CS.FAIL_TO_FAIL)
        elif pass_to_fail:
            self.finish(False, CS.PASS_TO_FAIL)
        elif not fail_to_pass:
            self.finish(False, CS.NO_FAIL_TO_PASS)
        else:
            self.finish(True, CS.SUCCESS)

    @property
    def py_bin(self):
        return self.venv_dir + "/bin/python"

    def make_main_py(self):
        py_main_cmd = " ".join(self.local_cfg.test_main.get_value())
        repo_py_test_main = REPO_DIR.child(self.repo).child("py_test_main.py")
        repo_py_test_main.write_if_not_exists(
            INPUTS_DIR.child("template/py_test_main.py").read_file()
        )
        print(repo_py_test_main)
        self.main_py_file.write_file(
            StrUtil().format(
                INPUTS_DIR.child("template/run_verification.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.cfg.base_commit.get_value(),
                INSTANCE_ID=self.cfg.instance_id.get_value(),
                content_category=self.cfg.content_category.get_value(),
                PY_BIN=self.py_bin,
                PY_TEST_MAIN_CODE=StrUtil().format(
                    repo_py_test_main.read_file(),
                    PY_MAIN_CMD=py_main_cmd,
                    PY_TEST_RESULT_JSON_FILE=CS.RESULT_JSON_FILE,
                ),
            )
        )

    def make_setup_env_sh(self):
        coda_cmd = "conda create -n testbed -y"
        if self.local_cfg.get_python_version() != "py3":
            coda_cmd += f" python={self.local_cfg.get_python_version()}"
        setup_env_sh = [
            f"cd {self.local_repo.path}",
            f"git reset --hard {self.cfg.base_commit.get_value()}",
            coda_cmd,
            "conda init",
            "conda activate testbed",
            f"python -m venv {self.venv_dir}",
            f"{self.py_bin} -m pip install --upgrade pip",
        ]
        local_env = REPO_DIR.child(f"{self.repo}/default/setup_env.sh")
        local_env.write_if_not_exists(
            f"pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist"
        )
        pyproject_toml = self.local_repo.child("pyproject.toml")
        setup_cfg = self.local_repo.child("setup.cfg")
        setup_py = self.local_repo.child("setup.py")
        if pyproject_toml.exists() or setup_cfg.exists() or setup_py.exists():
            setup_env_sh.append(f"{self.py_bin} -m pip install -e .")
        for d in local_env.read_line():
            if d.startswith("pip"):
                setup_env_sh.append(f"{self.py_bin} -m {d}")
            else:
                setup_env_sh.append(d)
        self.setup_env_sh.write_file("\n".join(setup_env_sh))
        self.logger.debug(f"sh {self.setup_env_sh.path}")

    def pip_install_pyproject_toml(self, f: File):
        data = f.get("project", "dependencies")
        ret = []
        if data:
            ret.extend([self.pkg_repair(v) for v in data])
        return ret

    def rest_repo(self, commid_id=None):
        """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
        if commid_id is None:
            commid_id = self.cfg.base_commit.get_value()
        self.git_cmd.reset(commid_id)
        self.git_cmd.clear()

    def make_patch(self):
        r = REPO_DIR.child(self.repo).child(self.name)
        test_patch = r.child("test.patch")
        code_patch = r.child("code.patch")
        if test_patch.exists():
            self.test_patch.f.write_file(test_patch.read_file())
        if code_patch.exists():
            self.code_patch.f.write_file(code_patch.read_file())

    def init(self):
        self.rest_repo()
        self.make_setup_repo_sh()
        self.make_setup_env_sh()
        self.make_main_py()
        self.make_patch()
        self.logger.debug(self.cfg.pr_url.get_value())
        self.logger.debug(self.cfg.issue_url.get_value())
        self.logger.debug(self.local_repo.path)
        self.logger.debug(f"{self.py_bin} {self.main_py_file.path}")

    def load(self):
        self.init()
        return self

    @property
    def venv_dir(self):
        return f"/.venv/{self.repo}/posix_{self.local_cfg.get_python_version()}"

    def run(self):
        error_msg, skip_msg = self.local_cfg.skip()
        if skip_msg:
            self.finish(True, error_msg)
            return
        self.init()
        if not self.local_cfg.test_main.get_value():
            self.finish(True, CS.NOT_FIND_CASES)
            return
        self.play()

    def play(self):
        pass

    def save(self):
        self.cfg.save()
        self.local_cfg.save()
