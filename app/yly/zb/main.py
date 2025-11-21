from common.util.export import ToolBase, File, logger, Dict, List, StrUtil
from common.tool.os_util import OsUtil
import os

INPUTS_DIR = "app/yly/zb"
REPO_BASE = "data/repo"


class ToolMain(ToolBase):
    def prepare(self, name):
        self.name: str = name
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
        self.change_py_test_files: List[File] = []

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
                if f.exists() and f.path.endswith(".py"):
                    self.change_py_test_files.append(f)

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

    def pip_install(self, exec_flag=True):
        raise Exception("todo")
        pip_packages = {"pytest-json-report"}
        set_up_file = self.local_repo.child("setup.cfg")
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
        setup_env_sh = []
        for pkg in pip_packages:
            if exec_flag:
                OsUtil(error_exit_flag=False).run("-m", "pip", "install", pkg)
            setup_env_sh.append(f"python -m pip install {pkg}")
        self.input_dir.child("setup_env.sh").write_file("\n".join(setup_env_sh))

    def apply_patch(self, f: File):
        self.get_update_file_by_batch(f)
        success, stdout, stderr = self.git_cmd.run("apply", f.get_abs_path())
        if not success:
            logger.error([stdout, stderr])

    def run_test(self):

        self.apply_patch(self.test_patch)

    def run_code(self):
        self.apply_patch(self.code_patch)

    def pkg_repair(self, pkg: str):
        if pkg.startswith("amazon_kclpy"):
            return
        return pkg.replace(";", ",").split(",")[0]

    def make_setup_repo_sh(self):
        self.input_dir.child("setup_repo.sh").write_file(
            "\n".join(
                [
                    f"mkdir -p {self.local_repo.parent().path}",
                    f"git clone {self.repo_uri} {self.local_repo.path}",
                ]
            )
        )

    def py_test(self):
        report_json_fp = self.local_repo.child(".report.json")
        if report_json_fp.exists():
            report_json_fp.remove()
        files = set(
            f.path.replace(self.local_repo.path + "/", "")
            for f in self.change_py_test_files
        )
        files.remove("tests/entrypoints/test_openai_server.py")
        OsUtil(error_exit_flag=True).set_env(self.local_repo.path).run(
            "-m", "pytest", "--json-report", *list(files)
        )

        ret = self.json_report_parse(report_json_fp)
        if not ret:
            raise Exception(files)
        return ret

    def print_result(self, old: dict, new: dict):
        for k in list(list(old.keys()) + list(new.keys())):
            old_statu, new_statu = old.get(k), new.get(k)
            if old_statu != new_statu:
                logger.info(f"{k} {old_statu}->{new_statu}")
            elif old_statu == new_statu and new_statu != "success":
                logger.info(f"{k} {old_statu}->{new_statu}")

    def install(self):
        OsUtil().run(self.setup_env_sh.path)

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                File(f"{INPUTS_DIR}/template.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.base_commit,
                INSTANCE_ID=self.config["instance_id"],
            )
        )

    veny_enable = False

    def make_env(self):
        if self.veny_enable:
            env_path = f"data/env_{os.name}/{self.name}"
            if not File(env_path).exists():
                OsUtil().run("-m", "venv", env_path)
            logger.info(f"attach env->{env_path}/Scripts/Activate.ps1")

    def main(self):
        self.make_setup_repo_sh()
        self.make_main_py()
        self.make_env()
        self.rest_repo()
        test_result = dict()
        self.run_test()
        # test_result = self.py_test()
        self.run_code()
        code_result = self.py_test()
        self.print_result(test_result, code_result)
        logger.info(self.local_repo.path)
        logger.info(f"python {self.main_py_file.path}")


if __name__ == "__main__":
    ToolMain().run()
