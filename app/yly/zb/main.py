from common.util.export import ToolBase, File, logger, Dict, List, StrUtil
from common.tool.os_util import OsUtil

INPUTS_DIR = "app/yly/zb"
REPO_BASE = "data/repo"


class ToolMain(ToolBase):
    def prepare(self, name):
        self.name: str = name
        self.input_dir = File(f"{INPUTS_DIR}/{name}")
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
        self.git_cmd.set_env(self.local_repo.path)

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

    def apply_patch(self, path):
        success, stdout, stderr = self.git_cmd.run("apply", path)
        if not success:
            logger.error([stdout, stderr])

    def apply_test_patch(self, *args, **kw):
        self.apply_patch(self.input_dir.child("test.patch").get_abs_path())

    def apply_code_patch(self, *args, **kw):
        self.apply_patch(self.input_dir.child("code.patch").get_abs_path())

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

    def make_main_py(self):
        self.main_py_file.write_file(
            StrUtil().format(
                File(f"{INPUTS_DIR}/template.py").read_file(),
                REPO_PATH=self.local_repo.path,
                BASE_COMMIT=self.base_commit,
                INSTANCE_ID=self.config["instance_id"],
            )
        )

    def init(self):
        self.make_main_py()
        self.prepare_repo()
        logger.info(self.local_repo.path)
        logger.info(f"python {self.main_py_file.path}")


if __name__ == "__main__":
    ToolMain().run()
