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
from .util import (
    INPUTS_DIR,
    INFO_DIR,
    REPO_BASE,
    Cg,
    task_cfg,
    TaskCfg,
    get_info_by_name,
    TASK_DIR,
    CS,
    TARGETS,
    get_result,
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
        self.cfg: Cg = Cg(self.task_id).set_resource(self.local_cfg.cg_file)
        self.owner, _, self.repo, self.pr_numer = get_info_by_name(
            self.local_cfg.name.get_value()
        )
        logger.info(self.local_cfg.resource)
        logger.info(self.cfg.resource)
        self.zip_file = self.input_dir.child(self.local_cfg.name.get_value() + ".zip")
        self.local_cfg.pr_url.set_value(self.cfg.pr_url.get_value())
        self.local_cfg.issue_url.set_value(self.cfg.issue_url.get_value())
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.local_repo = File(
            f"{REPO_BASE}/{self.cfg.repo.get_value()}"
        ).make_dir_if_not_exist()
        self.git_cmd = (
            GitUtil()
            .set_owner(self.owner)
            .set_repo(self.cfg.pr_url.get_value().split("/pull")[0] + ".git")
            .set_local_dir(self.local_repo)
            .clone()
        )
        self.pr = self.git_cmd.get_pr(self.pr_numer)
        self.setup_env_sh = self.input_dir.child("setup_env.sh")
        self.test_patch = self.pr.get_patch(self.input_dir.child("test.patch"))
        self.code_patch = self.pr.get_patch(self.input_dir.child("code.patch"))
        if not self.local_cfg.test_main.get_value():
            self.change_py_test_files: Dict[str, File] = dict()
            self.get_update_file_by_batch(self.test_patch)
            self.get_update_file_by_batch(self.code_patch)
            files = list(self.change_py_test_files.keys())
            self.local_cfg.test_main.set_value(" ".join(files))

        return self

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

    def rest_repo(self, commid_id=None):
        """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
        if commid_id is None:
            commid_id = self.cfg.base_commit.get_value()
        self.git_cmd.reset(commid_id)
        self.clear_repo()

    def clear_repo(self):
        self.git_cmd.clear()

    def apply_patch(self, f: Patch):
        if f.f.name == "test":
            data = self.cfg.test_patch.get_value()
        else:
            data = self.cfg.patch.get_value()
        data = data.replace("\r", "")
        f.f.write_file(data)
        logger.info(f"apply {f.f.get_abs_path()}")
        self.git_cmd.apply(f.f.get_abs_path())

    def make_setup_repo_sh(self):
        self.input_dir.child("setup_repo.sh").write_file(
            "\n".join(
                [
                    "set -e",
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git config --global http.sslVerify false",
                    f"git clone {self.git_cmd.repo} {self.local_repo.path}",
                    f"conda create -n testbed -y",
                ]
            )
        )

    def py_test(self, key) -> dict:
        f = Module().load_module_object(
            "run_verification.run_py_test", self.input_dir.path
        )
        statu_code, msg, msg1, ct, result = f()
        self.logger.debug(
            f"statu_code={statu_code}\nstdout={msg}\nstderr={msg1}\nresult={result}"
        )
        logger.info(f"{key}:{ct}")

    def re_init(self):
        self.input_dir.remove()
        File(self.input_dir.path + ".zip").unzip()
        self.init()

    def finish(self, statu, msgs):
        self.local_cfg.error_msg.set_value(msgs)
        self.save()
        # skip_file = self.input_dir.child("skip.txt").remove()
        # if skip_msg:
        #     skip_file.write_file(skip_msg)
        if statu:
            logger.info(f"ZB_TASK_SUCCESS {self.task_id} {self.zip_file} {msgs}")
            self.input_dir.zip(self.zip_file.path, TARGETS)
        else:
            msg = f"{CS.ZB_TASK_FAIL} {self.task_id} {self.zip_file} {msgs}"
            logger.info(msg)
            self.zip_file.remove()
            raise Exception(msg)

    def print_result(self):

        old, old_ct = get_result(self.input_dir.child("test.json").path)
        logger.info(f"test:{old_ct}")
        new, new_ct = get_result(self.input_dir.child("code.json").path)
        logger.info(f"code:{new_ct}")
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
        self.update_result(fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass)

    @property
    def py_bin(self):
        return self.venv_dir + "/bin/python"

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                INPUTS_DIR.child("run_verification.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.cfg.base_commit.get_value(),
                INSTANCE_ID=self.cfg.instance_id.get_value(),
                content_category=self.cfg.content_category.get_value(),
                PY_BIN=self.py_bin,
                PY_TEST_MAIN_CODE=StrUtil().format(
                    INPUTS_DIR.child("py_test_main.py").read_file(),
                    PY_MAIN_CMD=self.local_cfg.test_main.get_value(),
                    PY_TEST_RESULT_JSON_FILE=CS.RESULT_JSON_FILE,
                ),
            )
        )

    def update_result(self, fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass):
        local_result = dict()
        local_result["fail_to_fail"] = sorted(fail_to_fail)
        local_result["pass_to_fail"] = sorted(pass_to_fail)
        local_result["fail_to_pass"] = sorted(fail_to_pass)
        local_result["pass_to_pass"] = sorted(pass_to_pass)
        self.local_cfg.result.set_value(local_result)
        self.cfg.PASS_TO_PASS.set_value(pass_to_pass)
        self.cfg.FAIL_TO_PASS.set_value(fail_to_pass)
        if fail_to_fail:
            self.finish(False, CS.FAIL_TO_FAIL)
        elif pass_to_fail:
            self.finish(False, CS.PASS_TO_FAIL)
        elif not fail_to_pass:
            self.finish(False, CS.NO_FAIL_TO_PASS)
        else:
            self.finish(True, "")

    _dock_util = None

    @property
    def dock_util(self):
        if self._dock_util is None:
            from common.third_util.docker_util import DockerUtil

            self._dock_util = DockerUtil(self.local_cfg.docker_image_name.get_value())
        return self._dock_util

    def docker_build(self):
        self.dock_util.build(self.input_dir.get_abs_path(), f"{self.repo}:latest")

    def docker_verify(self, **kw):
        result_files = ["results.json", "test.json", "code.json"]
        for f in result_files:
            self.input_dir.child(f).remove()

        self.local_cfg.py_test_result_json.remove()
        status, msg = self.dock_util.run(
            ";".join(
                [
                    "/bin/bash -i -c 'cd /testbed && python run_verification.py",
                ]
                + [f"cp -f {f} /testbed_output/{f}" for f in result_files]
            )
            + "'",
            {
                self.code_patch.f.get_abs_path(): f"{REPO_BASE}/{self.code_patch.f.file_name}",
                self.test_patch.f.get_abs_path(): f"{REPO_BASE}/{self.test_patch.f.file_name}",
                self.main_py_file.get_abs_path(): f"{REPO_BASE}/{self.main_py_file.file_name}",
                # self.local_cfg.py_test_result_json.get_abs_path(): f"/testbed_output/{CS.RESULT_JSON_FILE}",
                self.input_dir.get_abs_path(): f"/testbed_output",
                self.local_repo.get_abs_path(): self.local_repo.path,
            },
            REPO_BASE,
            env={"INSTANCE_ID": self.cfg.instance_id.get_value()},
        )
        self.logger.debug(msg)

        if not status:
            self.print_result()
            # result_json = result_file.read_file()[self.cfg.instance_id.get_value()][
            #     "tests_status"
            # ]
            # self.update_result(
            #     result_json[CS.FAIL_TO_FAIL][CS.FAILURE],
            #     result_json[CS.PASS_TO_FAIL][CS.FAILURE],
            #     result_json[CS.FAIL_TO_PASS][CS.SUCCESS],
            #     result_json[CS.PASS_TO_PASS][CS.SUCCESS],
            # )
        else:
            self.finish(False, "UnKnow")

    def make_setup_env_sh(self):
        setup_env_sh = [
            f"cd {self.local_repo.path}",
            f"git reset --hard {self.cfg.base_commit.get_value()}",
            f"python -m venv {self.venv_dir}",
            f"{self.py_bin} -m pip install --upgrade pip",
        ]
        setup_env_sh.append(
            f"{self.py_bin} -m pip install pytest pytest-json-report toml debugpy"
        )
        pyproject_toml = self.local_repo.child("pyproject.toml")
        setup_cfg = self.local_repo.child("setup.cfg")
        setup_py = self.local_repo.child("setup.py")
        if pyproject_toml.exists() or setup_cfg.exists() or setup_py.exists():
            # setup_env_sh.extend(self.pip_install_pyproject_toml(pyproject_toml))
            # setup_env_sh.extend(self.pip_install_setup_cfg(setup_cfg))
            setup_env_sh.append(f"{self.py_bin} -m pip install .")
        pkgs: List[str] = self.local_cfg.setup_env.get_value()
        for pkg in pkgs:
            if pkg.endswith(".txt"):
                setup_env_sh.extend(
                    self.pip_install_requirements(self.local_repo.child(pkg))
                )
            else:
                setup_env_sh.append(pkg)

        self.setup_env_sh.write_file("\n".join(setup_env_sh))
        self.logger.debug(f"sh {self.setup_env_sh.path}")

    def pip_install_pyproject_toml(self, f: File):
        data = f.get("project", "dependencies")
        ret = []
        if data:
            ret.extend([self.pkg_repair(v) for v in data])
        return ret

    def init(self):
        self.rest_repo()
        self.make_setup_repo_sh()
        self.make_setup_env_sh()
        self.make_main_py()
        self.logger.debug(self.cfg.pr_url.get_value())
        self.logger.debug(self.cfg.issue_url.get_value())
        self.logger.debug(self.local_repo.path)
        self.logger.debug(f"{self.py_bin} {self.main_py_file.path}")

    @property
    def venv_dir(self):
        return f"/.venv/{self.repo}/posix_{self.local_cfg.py_name.get_value()}"

    def run0(self):
        self.rest_repo()
        self.py_test("pre")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.py_test("test")

    def run2(self, **kw):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        self.py_test("code")

    def can_skip_msg(self, msg):
        if msg in {CS.NOT_FIND_CASES}:
            return True
        return False

    def run(self, tp: str):
        error_msg = self.local_cfg.error_msg.get_value()
        if self.can_skip_msg(error_msg):
            self.finish(True, error_msg)
            return
        if self.zip_file.exists() and "ignore" in tp:
            logger.info(f"skip for {self.zip_file}  msg is {error_msg}")
            return
        self.init()
        if not self.local_cfg.test_main.get_value():
            self.finish(False, CS.NOT_FIND_CASES)
        elif self.local_cfg.docker_image_name.get_value() and "docker" in tp:
            self.docker_verify()
        else:
            self.verify_with_no_docker()

    def verify_with_no_docker(self):
        if not File(self.venv_dir).exists():
            OsUtil("python").set_venv(self.venv_dir)
            OsUtil("bash").run(self.setup_env_sh.get_abs_path())
        self.run1()
        self.run2()
        self.print_result()

    def save(self):
        self.cfg.save()
        self.local_cfg.save()
