import subprocess
from common.util.export import logger, Logger, File


class OsUtil:
    def check_output(self):
        return subprocess.check_output(
            self.get_cmd(),
            shell=True,
            stderr=self.logger.get_writer(),
            cwd=self.root_path,
        )

    def set_logger(self, logger):
        self.logger: File = logger
        return self

    def set_env(self, root, fun_name):
        self.root_path: str = root
        self.fun_name: str = fun_name
        return self

    def get_cmd(self):
        return f"{self.fun_name} {self.args}"

    def run(self, *args):
        self.args = " ".join(args)
        return self.check_output()
