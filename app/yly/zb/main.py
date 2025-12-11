from common.util.export import (
    ToolBase,
    File,
    logger,
    Dict,
    List,
    StrUtil,
    Module,
    get_log,
)
from common.tool.export import (
    OsUtil,
)

from .util import (
    INPUTS_DIR,
    REPO_BASE,
    Cg,
    TB,
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
        self.input_dir = File(path)

        if not self.input_dir.exists():
            self.input_dir = INPUTS_DIR.child(f"task/{path}")
        if not self.input_dir.exists():
            raise Exception(self.input_dir.path, "not exist")
        self.owner, self.task_id, self.repo, self.pr = get_info_by_name(
            self.input_dir.name
        )
        self.name: str = f"{self.owner}/{self.repo}"
        self.local_cfg = TB.get(self.input_dir.name)
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
        self.git_cmd = OsUtil("git")
        if not self.local_repo.exists():
            self.git_cmd.run("clone", self.repo_uri, self.local_repo.path)
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
        f.write_file(f.read_file().replace("\r", ""))
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
        self.logger.debug(f"get change_file_form patch {files}")
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

    def finish(self, statu, msgs, skip_msg=""):
        self.local_cfg.error_msg.set_value(msgs)
        if skip_msg:
            self.zip_file.parent().child("skip.txt").write_file(skip_msg)
        if statu:
            logger.info(f"{self.input_json.path} SUCCESS {skip_msg}")
            self.input_dir.zip(self.zip_file.path)
        else:
            logger.info(f"{self.input_json.path} FAIL")
            self.zip_file.parent().remove()
            raise Exception("FAIL", msgs)

    def print_result(self):
        result = self.local_cfg.result.get_value()
        old, new = result["test"], result["code"]
        f_to_p, p_to_p = (
            self.cfg.FAIL_TO_PASS.get_value(),
            self.cfg.PASS_TO_PASS.get_value(),
        )
        p_to_f = []
        f_to_p.clear()
        p_to_p.clear()
        for k in set(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                self.logger.debug(f"{k} {old_statu}->{new_statu}")
                if new_statu == PASSED:
                    f_to_p.append(k)
                else:
                    p_to_f.append(k)
            elif old_statu == new_statu and new_statu != PASSED:
                self.logger.debug(f"{k} {old_statu}->{new_statu}")
                p_to_p.append(k)

        if f_to_p and not p_to_f:
            self.finish(True, f"f_to_p:{f_to_p}")
        else:
            self.finish(False, f"f_to_p:{f_to_p} p_to_f:{p_to_f}")

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

    venv_enable = True

    docker_image_name = None

    def set_docker_image_name(self, image_name="zb:latest"):
        self.docker_image_name = image_name
        return self

    def update_result(self, fail_to_fail, pass_to_fail, fail_to_pass, pass_to_pass):
        local_result = self.local_cfg.result.get_value()
        local_result["fail_to_fail"] = fail_to_fail
        local_result["pass_to_fail"] = pass_to_fail
        local_result["fail_to_pass"] = fail_to_pass
        self.cfg.PASS_TO_PASS.set_value(pass_to_pass)
        if fail_to_pass and not fail_to_fail and not pass_to_fail:
            self.cfg.FAIL_TO_PASS.set_value(fail_to_pass)
            self.finish(True, "")
        else:
            self.finish(False, f"gg")

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
            "python -m pip install --upgrade pip",
            f"cd {self.local_repo.path}",
        ]
        pyproject_toml = self.local_repo.child("pyproject.toml")
        if pyproject_toml.exists():
            setup_env_sh.extend(self.pip_install_pyproject_toml(pyproject_toml))
        setup_cfg = self.local_repo.child("setup.cfg")
        if setup_cfg.exists():
            setup_env_sh.extend(self.pip_install_setup_cfg(setup_cfg))
        pkgs: List[str] = self.local_cfg.setup_env.get_value()
        for pkg in pkgs:
            if pkg.endswith(".txt"):
                setup_env_sh.extend(
                    self.pip_install_requirements(self.local_repo.child(pkg))
                )
            else:
                setup_env_sh.append(pkg)
        setup_env_sh.append("python -m pip install pytest pytest-json-report toml")
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
        pre_failes = [k for k, v in pre_result.items() if v != PASSED]
        if pre_failes:
            self.finish(False, f"pre_failed:{pre_failes}")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.py_test("test")

    def run2(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        self.py_test("code")
        self.print_result()

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
        try:
            if self.docker_image_name:
                self.docker_verify()
            else:
                self.verify_with_no_docker()
        except Exception as e:
            logger.debug(e, stack_info=True)

    def verify_with_no_docker(self):
        """
        o = OsUtil("python").set_venv(repo)
            o.run(
                "-m",
                "app.yly.zb.main",
                f.path.replace(".zip", ""),
                method,
                LOGER_PREFIX(repo),
            )
        """
        raise Exception("虚拟环境跑")
        self.setup_env()
        self.run0()
        self.run1()
        self.run2()

    def setup_env(self, **kw):
        raise Exception("第一次跑，在json里标记状态")
        OsUtil("sh").run(self.setup_env_sh.path)

    def exit(self):
        self.cfg.save()
        return super().exit()


if __name__ == "__main__":
    ZbTask().run()
