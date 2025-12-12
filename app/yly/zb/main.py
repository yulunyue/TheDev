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
from common.third_service.git_util import GitUtil
from .util import (
    INPUTS_DIR,
    INFO_DIR,
    REPO_BASE,
    Cg,
    TaskCfg,
    get_info_by_name,
    PASSED,
    PASS_TO_PASS,
    FAIL_TO_PASS,
    PASS_TO_FAIL,
    SUCCESS,
    FAILURE,
)

PIP_INSTALL_WITH_NO_DEPENDDS = {}

import os


class ZbTask(ToolBase):
    @property
    def logger(self):
        return get_log(f"zb/{self.repo}/{self.task_id}_{self.pr}")

    def prepare(self, path):
        if isinstance(path, str):
            self.input_dir = File(path)
            if not self.input_dir.exists():
                self.input_dir = INPUTS_DIR.child(f"task/{path}")
            if not self.input_dir.exists():
                self.input_dir = INPUTS_DIR.list_dir(
                    depth=3, filter=lambda v: path in v.name and v.type == "zip"
                )[0]
            if not self.input_dir.exists():
                raise Exception(self.input_dir.path, "not exist")
        else:
            self.input_dir = path
        if self.input_dir.type == "zip":
            self.input_dir = self.input_dir.unzip()
        self.owner, self.task_id, self.repo, self.pr = get_info_by_name(
            self.input_dir.name
        )
        self.name: str = f"{self.owner}/{self.repo}"
        self.local_cfg = TaskCfg(self.input_dir.name).set_resource(
            INFO_DIR.child(f"{self.input_dir.name}.json")
        )
        self.cfg: Cg = Cg(self.name)
        self.input_json = self.input_dir.child(
            f"{self.owner}__{self.repo}-{self.pr}.json"
        )
        self.zip_file = INPUTS_DIR.child(
            f"result/{self.task_id}/{self.input_json.name}.zip"
        ).make_dir_if_not_exist()

        self.cfg.set_resource(self.input_json)
        self.repo_uri = self.cfg.pr_url.get_value().split("/pull")[0] + ".git"
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.local_repo = File(
            f"{REPO_BASE}/{self.cfg.repo.get_value()}"
        ).make_dir_if_not_exist()
        self.git_cmd = GitUtil()
        if not self.local_repo.exists():
            self.git_cmd.clone(self.repo_uri, self.local_repo.path)
        self.setup_env_sh = self.input_dir.child("setup_env.sh")
        self.test_patch = self.input_dir.child("test.patch")
        self.code_patch = self.input_dir.child("code.patch")
        self.git_cmd.set_env(self.local_repo.path)
        self.change_py_test_files: Dict[str, File] = dict()
        self.get_update_file_by_batch(self.test_patch)
        self.get_update_file_by_batch(self.code_patch)
        return self

    def json_report_parse(self, fp: File):
        if not fp.exists():
            return dict()
        result = dict()
        data = fp.read_file()
        for item in data["tests"]:
            if item["nodeid"]:
                result[item["nodeid"]] = item["outcome"]
        fp.remove()
        return result

    def get_update_file_by_batch(self, fp: File):

        for s in fp.read_line():
            if s.startswith("+++ b/"):
                f = self.local_repo.child(s[6:])
                if f.path.endswith(".py") and f.name.startswith("test_"):
                    key = f.path.replace(self.local_repo.path + "/", "")
                    self.change_py_test_files[key] = f

    def rest_repo(self, commid_id=None):
        """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
        if commid_id is None:
            commid_id = self.cfg.base_commit.get_value()
        self.logger.debug(f"git reset {commid_id}")
        success, stdout, stderr = self.git_cmd.run("reset", "--hard", commid_id)
        if not success:
            self.finish(success, f"git reset fail")
            return False
        self.clear_repo()

    def clear_repo(self, *args, **kw):
        success, stdout, stderr = self.git_cmd.run("clean", "-fdx")
        if not success:
            self.logger.info([stdout, stderr])

    def pip_install_setup_cfg(self, set_up_file: File):

        pkgs: List[str] = []
        for section_name, depends in {
            "options": ["install_requires"],
            "options.extras_require": ["runtime", "test"],
        }.items():
            for dp in depends:
                lns = set_up_file.get(section_name, dp, default_value="").split("\n")
                for ln in lns:
                    pkg = self.pkg_repair(ln)
                    if not pkg:
                        continue
                    pkgs.append(pkg)
        return pkgs

    def pip_install_requirements(self, f: File):
        ret = []
        for ln in f.read_line():
            if not ln or ln.startswith("#"):
                continue
            pkg_install_cmd = self.pkg_repair(ln)
            if pkg_install_cmd:
                ret.append(pkg_install_cmd)
        return ret

    def apply_patch(self, f: File):
        if f.name == "test":
            data = self.cfg.test_patch.get_value()
        else:
            data = self.cfg.patch.get_value()
        data = data.replace("\r", "")
        f.write_file(data)
        self.logger.debug(f"apply {f.get_abs_path()}")
        self.git_cmd.run("apply", f.get_abs_path())

    def pkg_repair(self, pkg: str):
        if not pkg or pkg.startswith("#") or pkg.startswith("-"):
            return
        pkg = pkg.replace("#", ",").replace(";", ",").split(",")[0].replace(" ", "")
        if not pkg:
            return
        pkg_name, *version = pkg.replace("<=", "==").replace(">=", "==").split("=")
        flags = ["python -m pip install"]
        if pkg_name in PIP_INSTALL_WITH_NO_DEPENDDS:
            flags.append("--no-deps")
        flags.append(f'"{pkg}"')
        return " ".join(flags)

    def make_setup_repo_sh(self):
        self.input_dir.child("setup_repo.sh").write_file(
            "\n".join(
                [
                    "set -e",
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git config --global http.sslVerify false",
                    f"git clone {self.repo_uri} {self.local_repo.path}",
                    f"conda create -n testbed -y",
                ]
            )
        )

    def get_py_test_cmds(self):
        files = list(self.change_py_test_files.keys())
        logger.info(f"get change_file_form patch {files}")
        model_py_test = self.local_cfg.test_main.get_value()
        if model_py_test:
            return model_py_test
        return " ".join(files)

    def py_test(self, key) -> dict:
        report_json_fp = self.local_repo.child("result.json")
        if report_json_fp.exists():
            report_json_fp.remove()
        f = Module().load_module_object(
            "run_verification.run_py_test", self.input_dir.path
        )
        statu_code, msg, msg1 = f()
        result = self.local_cfg.result.get_value()
        result[key] = self.json_report_parse(report_json_fp)
        self.logger.debug(
            f"statu_code={statu_code}\nstdout={msg}\nstderr={msg1}\nresult={result[key]}"
        )
        return result[key]

    def make_patch(self, path: str, name):
        for p in path.split(" "):
            logger.info(self.local_repo.child(p))
        input(f"WAIT {name}")
        self.git_cmd.run("add", ".")
        self.git_cmd.run("config", "--global", "user.name", "xx", env=dict(HOME="./"))
        self.git_cmd.run(
            "config", "--global", "user.email", "xx@xx.com", env=dict(HOME="./")
        )
        self.git_cmd.run(
            "commit",
            "-m",
            name,
            env=dict(GIT_AUTHOR_NAME="xx", GIT_AUTHOR_EMAIL="xx@xx.com", HOME="./"),
        )
        # self.git_cmd.run("switch", "-c", f"zzb_{name}_branch")
        self.git_cmd.run("format-patch", "-1")
        ret = self.local_repo.child(f"0001-{name}.patch").read_file()
        return ret

    def re_init(self):
        self.input_dir.remove()
        File(self.input_dir.path + ".zip").unzip()
        self.init()

    def patch_repair(self, path=""):
        self.re_init()
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        data = self.make_patch(path, "test")
        self.test_patch.write_file(data)
        self.cfg.test_patch.set_value(data)
        data = self.make_patch(path, "code")
        self.code_patch.write_file(data)
        self.cfg.patch.set_value(data)

    def finish(self, statu, msgs, skip_msg=""):
        self.local_cfg.error_msg.set_value(msgs)
        self.exit()
        if skip_msg:
            self.zip_file.parent().child("skip.txt").write_file(skip_msg)
        if statu:
            logger.info(f"{self.input_json.path} SUCCESS {skip_msg}")
            self.input_dir.zip(self.zip_file.path)
        else:
            logger.info(f"{self.input_json.path} FAIL {msgs}")
            self.zip_file.parent().remove()
            raise Exception("FAIL", msgs)

    def print_result(self):
        result = self.local_cfg.result.get_value()
        old, new = result.get("test", dict()), result["code"]
        fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass = [], [], [], []

        for k in set(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                if new_statu == PASSED:
                    fail_to_pass.append(k)
                elif old_statu == PASSED:
                    pass_to_fail.append(k)
            elif old_statu == new_statu:
                if new_statu == PASSED:
                    pass_to_pass.append(k)
                else:
                    fail_to_fail.append(k)
        self.update_result(fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass)

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                INPUTS_DIR.child("run_verification.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.cfg.base_commit.get_value(),
                INSTANCE_ID=self.cfg.instance_id.get_value(),
                content_category=self.cfg.content_category.get_value(),
                PY_TEST_MAIN_CODE=StrUtil().format(
                    INPUTS_DIR.child("py_test_main.py").read_file(),
                    PY_MAIN_CMD=self.get_py_test_cmds(),
                ),
            )
        )

    docker_image_name = None

    def set_docker_image_name(self, image_name="zb:latest"):
        try:
            from common.third_util.docker_util import DockerUtil

            if DockerUtil(image_name).check_image_exists():
                self.docker_image_name = image_name
        except Exception as e:
            pass
        return self

    def docker_build(self, image_name="zb:latest"):
        from common.third_util.docker_util import DockerUtil

        self.init()
        DockerUtil(image_name).build(self.input_dir.get_abs_path())

    def update_result(self, fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass):
        local_result = self.local_cfg.result.get_value()
        local_result["fail_to_fail"] = fail_to_fail
        local_result["pass_to_fail"] = pass_to_fail
        local_result["fail_to_pass"] = fail_to_pass
        local_result["pass_to_pass"] = pass_to_pass
        self.cfg.PASS_TO_PASS.set_value(pass_to_pass)
        if fail_to_fail:
            self.finish(False, f"fail_to_fail")
        elif pass_to_fail:
            self.finish(False, f"path_to_fail")
        elif not fail_to_pass:
            self.finish(False, f"fail_to_pass")
        else:
            self.cfg.FAIL_TO_PASS.set_value(fail_to_pass)
            self.finish(True, "")

    def docker_verify(self, **kw):
        """
        OsUtil("python").run(INPUTS_DIR.child("verify.py").path, self.input_dir.path)
        """
        from common.third_util.docker_util import DockerUtil

        result_file = self.input_dir.child("result.json")
        result_file.remove()
        dock_util = DockerUtil(self.docker_image_name)
        status, msg = dock_util.run(
            "/bin/bash -i -c 'cd /testbed && python run_verification.py;cp -f results.json /testbed_output/result.json 2>/dev/null || true'",
            {
                self.code_patch.get_abs_path(): f"{REPO_BASE}/{self.code_patch.file_name}",
                self.test_patch.get_abs_path(): f"{REPO_BASE}/{self.test_patch.file_name}",
                self.main_py_file.get_abs_path(): f"{REPO_BASE}/{self.main_py_file.file_name}",
                self.input_dir.get_abs_path(): "/testbed_output",
            },
            REPO_BASE,
            env={"INSTANCE_ID": self.cfg.instance_id.get_value()},
        )
        self.logger.debug(msg)
        if result_file.exists():
            result_json = result_file.read_file()[self.cfg.instance_id.get_value()][
                "tests_status"
            ]
            self.update_result(
                result_json["FAIL_TO_FAIL"]["failure"],
                result_json["PASS_TO_FAIL"]["failure"],
                result_json["FAIL_TO_PASS"]["success"],
                result_json[PASS_TO_PASS][SUCCESS],
            )
        else:
            self.finish(False, "UnKnow")

    def make_setup_env_sh(self):
        setup_env_sh = [
            f"cd {self.local_repo.path}",
            f"git reset --hard {self.cfg.base_commit.get_value()}",
            "conda activate testbed",
            "python -m pip install --upgrade pip",
        ]
        setup_env_sh.append("python -m pip install pytest pytest-json-report toml")
        pyproject_toml = self.local_repo.child("pyproject.toml")
        setup_cfg = self.local_repo.child("setup.cfg")
        setup_py = self.local_repo.child("setup.py")
        if pyproject_toml.exists() or setup_cfg.exists() or setup_py.exists():
            # setup_env_sh.extend(self.pip_install_pyproject_toml(pyproject_toml))
            # setup_env_sh.extend(self.pip_install_setup_cfg(setup_cfg))
            setup_env_sh.append("python -m pip install .")
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
        self.logger.debug(f"python {self.main_py_file.path}")

    def run0(self):
        self.rest_repo()
        pre_result = self.py_test("pre")
        # pre_failes = [k for k, v in pre_result.items() if v != PASSED]
        # if pre_failes:
        #     self.finish(False, f"pre_failed:{pre_failes}")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        test_info = self.py_test("test")
        # test_failes = [k for k, v in test_info.items() if v != PASSED]
        # if not test_failes:
        #     self.finish(False, f"not test fail")

    def run2(self, **kw):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        self.py_test("code")

    def execute(self):
        if self.docker_image_name:
            self.docker_verify()
        else:
            self.verify_with_no_docker()

    def main(self, **kw):
        error_msg = self.local_cfg.error_msg.get_value()
        if self.zip_file.exists() and not error_msg:
            return
        self.init()
        skip = self.local_cfg.skip.get_value()
        if skip and not error_msg:
            if isinstance(skip, str):
                self.finish(True, "", skip_msg=skip)
            return
        logger.run_capture_error(self.execute)

    def verify_with_no_docker(self):
        """
        {env_path}/Scripts/Activate.ps1
        o.run(
            "-m",
            "app.yly.zb.main",
            f.path.replace(".zip", ""),
            method,
            LOGER_PREFIX(repo),
        )
        """
        o = OsUtil("python")
        if self.local_cfg.need_setup_env.get_value():
            self.setup_env()
            self.local_cfg.need_setup_env.set_value(False)
        self.run0()
        self.run1()
        self.run2()
        self.print_result()

    def setup_env(self, **kw):
        OsUtil("sh").run(self.setup_env_sh.path)

    def save(self):
        self.cfg.save()
        self.local_cfg.save()

    def exit(self):
        self.save()


if __name__ == "__main__":
    ZbTask().run()
