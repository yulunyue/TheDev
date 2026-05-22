import subprocess
from common.util.export import (
    File,
    TheDevLogger,
    get_dev_log,
    logger,
    Thread,
    List,
    os,
    sys,
)


class OsUtil:
    time_out = 3600

    def __init__(self, fun_name: str, error_exit_flag=True):
        self.fun_name = fun_name.replace("\\", "/")
        self.error_exit_flag = error_exit_flag
        self.root_path = "./"
        self.and_cmds = []

    _logger: TheDevLogger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger: TheDevLogger = get_dev_log(
                f"data/log/os/{self.fun_name.split('/').pop()}"
            )  # 用TheDev 主要是方便writer 重定向
        return self._logger

    def set_time_out(self, timeout):
        self.timeout = timeout
        return self

    def set_venv(self, env_path):
        local_exec = sys.executable.replace("\\", "/")
        if env_path in local_exec:
            return
        if not File(env_path).exists():
            OsUtil("python").run("-m", "venv", env_path)
        if os.name == "nt":
            cmd = f"{env_path}/Scripts/Activate.ps1"
        else:
            cmd = f"source {env_path}/bin/activate"
        logger.info(f"请用  {cmd} 进入虚拟环境执行 {local_exec}")

    def check_output(self, cmd: List[str], env=None):
        cmds = " ".join(cmd)
        self.logger.info(f"{self.root_path}->{cmds}")
        param = dict()
        param.update(
            dict(
                stderr=self.logger.get_writer(),
                stdout=self.logger.get_writer(),
            )
        )
        try:
            self.process = subprocess.Popen(
                cmd,
                # check=True,
                shell=False,
                # capture_output=capture_output,
                text=True,
                cwd=self.root_path,
                # timeout=self.time_out,
                env=env,  # 不能为空字典 [WinError 87] 参数错误。
                **param,
            )

            self.process.wait(self.time_out)
            data = self.logger.fp.read_file()
            statu, stdout, stderror = self.process.returncode == 0, data, data
        except subprocess.CalledProcessError as e:
            statu, stdout, stderror = False, e.stdout, e.stderr
        except FileNotFoundError:
            statu, stdout, stderror = False, "", f"Command '{cmd[0]}' not found."
        except Exception as e:
            statu, stdout, stderror = False, "", f"{e}"
        if not statu:
            self.error(cmds, stdout + stderror)
        return statu, stdout, stderror

    def error(self, cmd, msg):
        if self.error_exit_flag:
            raise Exception(cmd, msg)
        else:
            logger.info(msg[:20] + "..." + msg[-20:] + cmd)

    def set_logger(self, logger):
        if isinstance(logger, str):
            logger = get_dev_log(logger)
        self._logger: TheDevLogger = logger
        return self

    def set_env(self, root):
        self.root_path: str = root
        return self

    def get_cmd(self, args, kw: dict):
        ret: List[str] = [self.fun_name] + list(args)
        for k, v in kw.items():
            ret.extend([k, v])
        return ret

    def popen_output(self, *args, timeout=60, env=None, **kw) -> str:
        """
        执行命令并返回 stdout 内容

        参数：
        - timeout: 超时时间（默认 60 秒）
        - env: 环境变量

        返回：stdout 内容（失败返回空字符串，或根据 error_exit_flag 抛异常）
        """
        proc = self.popen(*args, env=env, **kw)
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            if proc.returncode == 0:
                return stdout.strip()
            else:
                cmds = " ".join(self.get_cmd(args, kw))
                error_msg = stderr.strip() or stdout.strip()
                self.error(cmds, error_msg)
                return ""
        except subprocess.TimeoutExpired:
            proc.kill()
            cmds = " ".join(self.get_cmd(args, kw))
            self.error(cmds, "timeout")
            return ""
        except Exception as e:
            cmds = " ".join(self.get_cmd(args, kw))
            self.error(cmds, str(e))
            return ""

    def run(self, *args, env=None, **kw):
        return self.check_output(self.get_cmd(args, kw), env=env)

    def start(self, *args, **kw):
        Thread(target=self.run, args=args, kwargs=kw).start()
        return self

    def stop(self):
        self.process.kill()

    def system(self, *args, **kw):
        cmd = " ".join(self.get_cmd(args, kw))
        self.logger.info(cmd)
        ret = os.system(cmd)
        if ret:
            self.error(cmd)

    def new_exec(self, *args):
        cmd = self.get_cmd(args)
        self.logger.info(cmd)
