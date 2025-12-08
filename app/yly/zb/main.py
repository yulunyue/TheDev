from common.util.export import ToolBase, File, logger, Dict, List, StrUtil, Module
from common.tool.export import (
    OsUtil,
    ConfigBase,
    TableBase,
    StrModel,
    ListModel,
    DictModel,
)


class Cg(ConfigBase):
    test_main = StrModel()
    setup_env = ListModel()
    result = DictModel()
    after_setup_env = DictModel()
    base_commit = StrModel()
    pr_url = StrModel()
    repo = StrModel()
    instance_id = StrModel()
    issue_url = StrModel()
    code_commit = StrModel(default_value="code.patch")
    language = StrModel(default_value="python")
    FAIL_TO_PASS = ListModel()
    PASS_TO_PASS = ListModel()
    content_category = StrModel(
        default_value="其他"
    )  # 计算、通⽤、⼯具、可视化、系统、时间、⽹络、加密、其他


PIP_INSTALL_WITH_NO_DEPENDDS = {}

import os

INPUTS_DIR = "app/yly/zb"
REPO_BASE = "data/repo"


class ToolMain(ToolBase):
    def prepare(self, name):
        self.name: str = name
        self.cfg: Cg = Cg(name)
        self.cfg.set_resource(f"{INPUTS_DIR}/{name}/{name}.json")
        self.input_dir = File(f"{INPUTS_DIR}/{name}")
        if not self.input_dir.exists():
            File(self.input_dir.path + ".zip").unzip()

        self.repo_uri = self.cfg.pr_url.get_value().split("/pull")[0] + ".git"
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.py_test_main_py = self.input_dir.child("py_test_main.py")
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

    def json_report_parse(self, fp: File):
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
        success, stdout, stderr = self.git_cmd.run("reset", "--hard", commid_id)
        if not success:
            logger.info([stdout, stderr])
            return False
        self.clear_repo()

    def clear_repo(self, *args, **kw):
        success, stdout, stderr = self.git_cmd.run("clean", "-fdx")
        if not success:
            logger.info([stdout, stderr])

    def init_setup_cfg(set_up_file):
        pip_packages = []
        if set_up_file.exists():
            pkgs: List[str] = []
            for section_name, depends in {
                "options": ["install_requires"],
                "options.extras_require": ["runtime", "test"],
            }.items():
                for dp in depends:
                    pkgs.extend(
                        set_up_file.get(section_name, dp, default_value="").split("\n")
                    )
            for pkg in pkgs:
                pkg = self.pkg_repair(pkg)
                if not pkg:
                    continue
                pip_packages.add(pkg)

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
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git clone {self.repo_uri} {self.local_repo.path}",
                ]
            )
        )

    def get_py_test_cmds(self):
        files = list(self.change_py_test_files.keys())
        logger.info(f"get change_file_form patch {files}")
        model_py_test = self.cfg.test_main.get_value()
        if model_py_test:
            return model_py_test
        return " ".join(files)

    def py_test(self, key):
        report_json_fp = self.local_repo.child("result.json")
        if report_json_fp.exists():
            report_json_fp.remove()
        f = Module().load_module_object(
            "run_verification.run_py_test", self.input_dir.path
        )
        statu_code, msg, msg1 = f()
        logger.debug(f"statu_code={statu_code},msg={msg},msg1={msg1}")
        result = self.cfg.result.get_value()
        result[key] = self.json_report_parse(report_json_fp)

    def print_result(self):
        result = self.cfg.result.get_value()
        old, new = result["test"], result["code"]
        f_to_p, p_t_p = (
            self.cfg.FAIL_TO_PASS.get_value(),
            self.cfg.PASS_TO_PASS.get_value(),
        )
        for k in list(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                logger.info(f"{k} {old_statu}->{new_statu}")
                if new_statu == "passed":
                    f_to_p.append(k)
            elif old_statu == new_statu and new_statu != "passed":
                logger.info(f"{k} {old_statu}->{new_statu}")
                p_t_p.append(k)

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                File(f"{INPUTS_DIR}/{self.main_py_file.name}.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.cfg.base_commit.get_value(),
                INSTANCE_ID=self.cfg.instance_id.get_value(),
                CODE_PATCH=self.cfg.code_commit.get_value(),
                content_category=self.cfg.content_category.get_value(),
            )
        )
        self.py_test_main_py.write_file(
            StrUtil().format(
                File(f"{INPUTS_DIR}/{self.py_test_main_py.name}.py").read_file(),
                PY_MAIN_CMD=self.get_py_test_cmds(),
            )
        )

    venv_enable = True

    def make_env(self):
        if not self.venv_enable:
            return
        name = self.name.split("-")[0]
        env_path = f"data/env_{os.name}/{name}"
        if not File(env_path).exists():
            OsUtil().run("-m", "venv", env_path)
        if os.name == "nt":
            logger.info(f"{env_path}/Scripts/Activate.ps1")
        else:
            logger.info(f"source {env_path}/bin/activate")

    def make_setup_env_sh(self):
        setup_env_sh = [
            "python -m pip install --upgrade pip",
            f"cd {self.local_repo.path}",
        ]
        pyproject_toml = self.local_repo.child("pyproject.toml")
        if pyproject_toml.exists():
            setup_env_sh.extend(self.pip_install_pyproject_toml(pyproject_toml))
        pkgs: List[str] = self.cfg.setup_env.get_value()
        for pkg in pkgs:
            if pkg.endswith(".txt"):
                setup_env_sh.extend(
                    self.pip_install_requirements(self.local_repo.child(pkg))
                )
            else:
                setup_env_sh.append(pkg)
        setup_env_sh.append("python -m pip install pytest pytest-json-report toml")
        self.setup_env_sh.write_file("\n".join(setup_env_sh))
        logger.info(f"sh {self.setup_env_sh.path}")

    def pip_install_pyproject_toml(self, f: File):
        data = f.get("project", "dependencies")
        return [self.pkg_repair(v) for v in data]

    def make_zip(self):
        zip_file = self.input_dir.child(f".zip")
        if zip_file.exists():
            zip_file.remove()
        self.input_dir.zip()

    def init(self):
        self.pre2()
        self.make_setup_repo_sh()
        self.make_setup_env_sh()
        self.make_main_py()
        self.make_env()
        self.make_zip()
        logger.info(self.cfg.pr_url.get_value())
        logger.info(self.cfg.issue_url.get_value())
        logger.info(self.local_repo.path)
        logger.info(f"python {self.main_py_file.path}")

    def run0(self):
        self.rest_repo()
        self.py_test("test")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.py_test("test")

    def pre2(self):
        code_commit = self.cfg.code_commit.get_value()
        if code_commit.endswith(".patch"):
            self.rest_repo()
            self.apply_patch(self.test_patch)
            self.apply_patch(self.code_patch)
        else:
            self.rest_repo(code_commit)

    def run2(self):
        self.pre2()
        self.py_test("code")

    def main(self):
        self.init()
        self.run1()
        self.run2()
        self.print_result()

    def setup_env(self):
        OsUtil("sh").run(self.setup_env_sh.path)

    def exit(self):
        self.cfg.save()


if __name__ == "__main__":
    ToolMain().run()
