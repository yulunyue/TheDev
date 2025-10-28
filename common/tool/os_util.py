import subprocess
from common.util.export import File, TheDevLoger, get_dev_log

logger = get_dev_log("os")


class OsUtil:
    def __init__(self, fun_name):
        self.fun_name = fun_name
        self.root_path = "./"
        self.logger: TheDevLoger = logger  # 用TheDev 主要是方便writer 重定向

    def check_output(self):
        cmd = self.get_cmd()
        self.logger.info(cmd)
        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=self.logger.get_writer(),
            cwd=self.root_path,
        )

    def run(self):
        subprocess.run()

    def set_logger(self, logger):
        self.logger: TheDevLoger = logger
        return self

    def set_env(self, root, fun_name):
        self.root_path: str = root
        self.fun_name: str = fun_name
        return self

    def get_cmd(self):
        return f"{self.fun_name} {self.args}"

    def run(self, *args):
        self.args = " ".join(args)
        return self.check_output().decode()
