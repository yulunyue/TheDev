import subprocess
from common.util.export import File, TheDevLoger, get_dev_log, logger
import os
import sys
import re


class OsUtil:
    def __init__(self, fun_name=None, error_exit_flag=True):
        self.fun_name = fun_name or sys.executable
        self.error_exit_flag = error_exit_flag
        self.root_path = "./"
        self.logger: TheDevLoger = get_dev_log(
            f"data/log/os/{self.fun_name.split('/').pop()}"
        )  # 用TheDev 主要是方便writer 重定向

    def check_output(self, cmds=None, capture_output=False):
        if cmds is None:
            cmds = self.get_cmd()
        self.logger.info(f"{self.root_path}->{cmds}")
        cmd = [v for v in cmds.split(" ") if v]
        param = dict()
        if not capture_output:
            param.update(
                dict(
                    stderr=self.logger.get_writer(),
                    stdout=self.logger.get_writer(),
                )
            )
        try:
            process = subprocess.run(
                cmd,
                check=True,
                capture_output=capture_output,
                text=True,
                cwd=self.root_path,
                timeout=60 * 60,
                **param,
            )
            statu, stdout, stderror = True, process.stdout, process.stderr
        except subprocess.CalledProcessError as e:
            statu, stdout, stderror = False, e.stdout, e.stderr
        except FileNotFoundError:
            statu, stdout, stderror = False, "", f"Command '{cmd[0]}' not found."
        except Exception as e:
            statu, stdout, stderror = False, "", f"{e}"
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

    def check_port_with_netstat(self, port):
        statu, result, stderror = self.check_output("netstat -ano", capture_output=True)

        # 查找端口
        pattern = rf":{port}\s+"
        for line in result.split("\n"):
            if re.search(pattern, line):
                return line.strip()
        return ""

    def check_port(self, port):
        return self.check_port_with_netstat(port)
