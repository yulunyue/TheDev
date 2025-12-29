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
    json_dumps,
)
from common.tool.export import OsUtil, GC
from common.third_service.git_tool.git_util import GitUtil, Patch
from ..model.export import (
    INPUTS_DIR,
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

PIP_MAP = REPO_DIR.child("pip.json").read_file()


class ZbTask:
    local_cfg: TaskCfg = None

    @property
    def logger(self):
        return get_log(f"zb/{self.repo}/{self.task_id}_{self.local_cfg.pr}")

    def build(self, local_cfg):
        if self.local_cfg:
            raise Exception("init twitch")
        self.local_cfg: TaskCfg = local_cfg

        if not self.local_cfg.resource.exists():
            raise Exception(f"{self.local_cfg.resource} not exist")
        self.name, self.task_id = self.local_cfg.name.get_value(), self.local_cfg.key
        self.input_dir = self.local_cfg.input_dir
        if not self.input_dir.exists():
            raise Exception(self.input_dir.path, "not exist")
        self.owner, _, self.repo, self.pr_numer = get_info_by_name(
            self.local_cfg.name.get_value()
        )
        logger.info(self.local_cfg.cg.resource)
        logger.info(self.local_cfg.resource)
        self.local_repo = self.local_cfg.local_repo
        self.zip_file = self.input_dir.child(self.local_cfg.name.get_value() + ".zip")
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.setup_env_sh = self.input_dir.child("setup_env.sh")
        return self

    def apply_patch(self, f: Patch):
        self.local_cfg.git_cmd.apply(f.f.get_abs_path())

    has_apply_code = False

    def apply_code(self):
        if self.has_apply_code:
            raise Exception("apply code only one")
        self.has_apply_code = True
        self.rest_repo()
        self.apply_patch(self.local_cfg.test_patch)
        self.apply_patch(self.local_cfg.code_patch)
        return self

    has_apply_test = False

    def apply_test(self):
        if self.has_apply_test:
            raise Exception("apply test only one")
        self.has_apply_test = True
        self.rest_repo()
        self.apply_patch(self.local_cfg.test_patch)
        return self

    def re_init(self):
        self.input_dir.remove()
        File(self.input_dir.path + ".zip").unzip()
        self.init()

    def print_result(self):
        local_result: dict = self.local_cfg.result.get_value()
        local_result.clear()
        old, old_ct, local_result["old_detail"] = get_result(
            self.input_dir.child("test.json").path
        )
        test_log = self.input_dir.child("test.log")
        code_log = self.input_dir.child("code.log")
        logger.info(f"test:{old_ct}, {test_log}")
        new, new_ct, local_result["new_detail"] = get_result(
            self.input_dir.child("code.json").path
        )
        logger.info(f"code:{new_ct}, {code_log}")
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
        t = self.local_cfg
        if fail_to_fail:
            self.local_cfg.set_error_msg(CS.FAILED, CS.FAIL_TO_FAIL)
        elif pass_to_fail:
            self.local_cfg.set_error_msg(CS.FAILED, CS.PASS_TO_FAIL)
        elif old_ct == new_ct and old_ct:
            self.local_cfg.set_error_msg(
                CS.SKIPPED, f"{CS.TEST_RESULT_NO_CHANGE}={old_ct} --> {new_ct}"
            )
        elif not fail_to_pass:
            self.local_cfg.set_error_msg(CS.FAILED, CS.NO_FAIL_TO_PASS)
        elif not pass_to_pass:
            t.set_error_msg(CS.FAILED, CS.NO_PASS_TO_PASS)
        elif new_ct.get("error"):
            t.set_error_msg(CS.FAILED, f"CODE_WITH_ERROR")
        elif new_ct.get("failed"):
            t.set_error_msg(CS.FAILED, f"CODE_WITH_FAILED")
        elif self.__class__.__name__ != "DockerTask":
            t.set_error_msg(CS.FAILED, f"WINDOWS_ERROR")
        else:
            self.local_cfg.set_error_msg(CS.SUCCESS, "")
        self.save()

    @property
    def py_bin(self):
        return "conda run -n testbed python"
        return self.venv_dir + "/bin/python"

    def get_py_test_main_code(self):
        py_main_cmd = " ".join(self.local_cfg.test_main.get_value())
        return py_main_cmd

    def make_main_py(self):
        RUN_BEFORE_PY_TEST = ""
        files = [
            self.local_cfg.local_repo_mock_dir,
            INPUTS_DIR.child(f"template"),
        ]
        for f in files:
            if f.child(CS.RUN_VERIFICATION_PY).exists():
                RUN_BEFORE_PY_TEST = f.child(CS.RUN_VERIFICATION_PY).read_file()
                break
        self.main_py_file.write_file(
            StrUtil().format(
                RUN_BEFORE_PY_TEST,
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.local_cfg.cg.base_commit.get_value(),
                INSTANCE_ID=self.local_cfg.cg.instance_id.get_value(),
                content_category=self.local_cfg.cg.content_category.get_value(),
                PY_BIN="python",
                PY_MAIN_CMD=self.get_py_test_main_code(),
            )
        )

    def make_setup_repo_sh(self):
        coda_cmd = f"conda create -n testbed -y python={self.local_cfg.py_version}"
        self.input_dir.child("setup_repo.sh").write_file(
            "\n".join(
                [
                    "set -e",
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git config --global http.sslVerify false",
                    f"git clone {self.local_cfg.repo_uri} {self.local_repo.path}",
                    coda_cmd,
                ]
            )
        )

    def make_setup_env_sh(self):
        local_env_sh: List[str] = [
            "set -e",
            f"cd {self.local_repo.path}",
            f"git reset --hard {self.local_cfg.cg.base_commit.get_value()}",
            f"{self.py_bin} --version",
        ]
        if GC.pip_global_index_url.get_value():
            local_env_sh.extend(
                [
                    f"pip config set global.index-url {GC.pip_global_index_url.get_value()}",
                    f"pip config set global.trusted-host {GC.pip_trusted_host.get_value()}",
                ]
            )

        f = self.local_cfg.env_dir.child("setup_env.sh")
        local_env_sh.extend(f.read_line())
        local_env_sh.append(
            "pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist"
        )
        setup_env_sh = []
        for d in local_env_sh:
            if d.startswith("pip"):
                setup_env_sh.append(f"{self.py_bin} -m {d}")
            else:
                setup_env_sh.append(d)
        self.setup_env_sh.write_file("\n".join(setup_env_sh))
        self.logger.debug(f"sh {self.setup_env_sh.path}")

    def make_launch_json(self):
        info = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "remote_debug_docker",
                    "type": "debugpy",
                    "request": "attach",
                    "connect": {"host": "localhost", "port": 5678},
                    "pathMappings": [
                        {
                            "localRoot": self.local_repo.get_abs_path(),
                            "remoteRoot": self.local_repo.path,
                        }
                    ],
                    "justMyCode": False,
                }
            ],
        }
        self.local_repo.child(".vscode/launch.json").write_file(info)
        self.local_repo.child("py_test_main.py").write_file(
            StrUtil().format(
                INPUTS_DIR.child("template/py_test_main.py").read_file(),
                PY_MAIN_CMD=self.get_py_test_main_code(),
            )
        )
        return self

    def rest_repo(self, commid_id=None):
        """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
        if commid_id is None:
            commid_id = self.local_cfg.cg.base_commit.get_value()
        self.local_cfg.git_cmd.reset(commid_id)
        self.local_cfg.git_cmd.clear()

    def make_patch(self):
        r = REPO_DIR.child(self.repo).child("pr").child(self.name)
        test_patch = r.child("test.patch")
        code_patch = r.child("code.patch")
        if test_patch.exists():
            self.local_cfg.test_patch.f.write_file(test_patch.read_file())
        if code_patch.exists():
            self.local_cfg.code_patch.f.write_file(code_patch.read_file())

    def init(self):
        self.make_setup_repo_sh()
        self.make_setup_env_sh()
        self.make_main_py()
        self.logger.debug(self.local_cfg.pr_url.get_value())
        self.logger.debug(self.local_cfg.issue_url.get_value())
        self.logger.debug(self.local_repo.path)
        self.logger.debug(f"{self.py_bin} {self.main_py_file.path}")

    def load(self):
        self.init()
        return self

    @property
    def venv_dir(self):
        return f"/.venv/{self.repo}/posix_{self.local_cfg.py_env}"

    def run(self):
        self.init()
        self.play()

    def play(self):
        pass

    def save(self):
        self.local_cfg.cg.save()
        self.local_cfg.save()
