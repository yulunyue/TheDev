import subprocess
from common.util.export import File, TheDevLoger, get_dev_log, logger
import os
import sys


class OsUtil:
    def __init__(self, fun_name=None, error_exit_flag=True):
        self.fun_name = fun_name or sys.executable
        self.error_exit_flag = error_exit_flag
        self.root_path = "./"
        self.logger: TheDevLoger = get_dev_log("os")  # 用TheDev 主要是方便writer 重定向

    def check_output(self):
        cmds = self.get_cmd()
        self.logger.info(f"{self.root_path}->{cmds}")
        cmd = [v for v in cmds.split(" ") if v]
        try:
            process = subprocess.run(
                cmd,
                check=True,
                capture_output=False,
                text=True,
                cwd=self.root_path,
                stderr=self.logger.get_writer(),
                stdout=self.logger.get_writer(),
                timeout=20 * 60,
            )
            statu, stdout, stderror = True, process.stdout, process.stderr
        except subprocess.CalledProcessError as e:
            statu, stdout, stderror = False, e.stdout, e.stderr
        except FileNotFoundError:
            statu, stdout, stderror = False, "", f"Command '{cmd[0]}' not found."
        if not statu:
            self.error([cmds, stdout, stderror])
        return statu, stdout, stderror

    def error(self, msg):
        if self.error_exit_flag:
            raise Exception(msg)
        else:
            logger.error(msg)

    def set_logger(self, logger):
        self.logger: TheDevLoger = logger
        return self

    def set_env(self, root):
        self.root_path: str = root
        return self

    def get_cmd(self):
        return f"{self.fun_name} {self.args}"

    def run(self, *args):
        self.args = " ".join(args)
        return self.check_output()

    def system(self, *args):
        self.args = " ".join(args)
        cmd = f"{self.fun_name} {self.args}"
        self.logger.info(cmd)
        ret = os.system(cmd)
        if ret:
            self.error(cmd)
