from common.util.export import ToolBase, File, logger, Dict, List, StrUtil
from common.tool.export import (
    OsUtil,
    TableConfig,
    TableBase,
    StrModel,
    ListModel,
    DictModel,
)


class Task(TableConfig):
    test_main = StrModel()
    setup_env = ListModel()
    result = DictModel()


import os

INPUTS_DIR = "app/yly/zb"
REPO_BASE = "data/repo"

CONFIG_RESOURCE = TableBase[Task]().set_resource("zb")


class ToolMain(ToolBase):
    def prepare(self, name):
        self.name: str = name
        self.model = CONFIG_RESOURCE.get(name)
        self.input_dir = File(f"{INPUTS_DIR}/{name}")
        if not self.input_dir.exists():
            File(self.input_dir.path + ".zip").unzip()
        self.config_json_file = self.input_dir.child(f"{name}.json")
        self.config: Dict[str, str] = self.config_json_file.read_file()
        self.base_commit = self.config["base_commit"]
        self.repo_uri = self.config["pr_url"].split("/pull")[0] + ".git"
        self.main_py_file = self.input_dir.child("run_verification.py")
        self.local_repo = File(
            f"{REPO_BASE}/{self.config['repo']}"
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

    def rest_repo(self):
        """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
        success, stdout, stderr = self.git_cmd.run("reset", "--hard", self.base_commit)
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

    def apply_patch(self, f: File):
        self.git_cmd.run("apply", f.get_abs_path())

    def pkg_repair(self, pkg: str):
        pkg = pkg.replace(";", ",").split(",")[0].replace(" ", "")
        return f"python -m pip install {pkg}"

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
        model_py_test = self.model.test_main.get_value()
        if model_py_test:
            return model_py_test
        return " ".join(files)

    def py_test(self, key):
        report_json_fp = self.local_repo.child(".report.json")
        if report_json_fp.exists():
            report_json_fp.remove()
        OsUtil(error_exit_flag=False).set_env(self.local_repo.path).run(
            "-m", "pytest", "--json-report", self.get_py_test_cmds()
        )
        result = self.model.result.get_value()
        result[key] = self.json_report_parse(report_json_fp)

    def print_result(self):
        result = self.model.result.get_value()
        old, new = result["test"], result["code"]
        for k in list(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                logger.info(f"{k} {old_statu}->{new_statu}")
            elif old_statu == new_statu and new_statu != "passed":
                logger.info(f"{k} {old_statu}->{new_statu}")

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                File(f"{INPUTS_DIR}/template.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.base_commit,
                INSTANCE_ID=self.config["instance_id"],
                PY_MAIN_CMD=self.get_py_test_cmds(),
            )
        )

    venv_enable = True

    def make_env(self):
        if not self.venv_enable:
            return
        env_path = f"data/env_{os.name}/{self.name}"
        if not File(env_path).exists():
            OsUtil().run("-m", "venv", env_path)
        if os.name == "nt":
            logger.info(f"{env_path}/Scripts/Activate.ps1")
        else:
            logger.info(f"source {env_path}/bin/activate")

    def make_setup_env_sh(self):
        etup_env_sh = [
            "python -m pip install --upgrade pip",
            "python -m pip install pytest pytest-json-report toml",
            f"cd {self.local_repo.path}",
        ]
        etup_env_sh.extend(self.model.setup_env.get_value())
        pyproject_toml = self.local_repo.child("pyproject.toml")
        if pyproject_toml.exists():
            etup_env_sh.extend(self.pip_install_pyproject_toml(pyproject_toml))
        self.setup_env_sh.write_file("\n".join(etup_env_sh))
        logger.info(f"sh {self.setup_env_sh.path}")

    def pip_install_pyproject_toml(self, f: File):
        data = f.get("project", "dependencies")
        return [self.pkg_repair(v) for v in data]

    def init(self):
        self.make_setup_repo_sh()
        self.make_setup_env_sh()
        self.make_main_py()
        self.make_env()
        logger.info(self.config.get("pr_url"))
        logger.info(self.config.get("issue_url"))
        logger.info(self.local_repo.path)
        logger.info(f"python {self.main_py_file.path}")

    def run1(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.py_test("test")

    def run2(self):
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        self.py_test("code")

    def main(self):
        self.init()
        self.run1()
        self.run2()
        self.print_result()


if __name__ == "__main__":
    ToolMain().run()
    CONFIG_RESOURCE.save()
