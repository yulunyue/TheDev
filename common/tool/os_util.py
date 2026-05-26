import subprocess
from common.util.export import (
    File,
    TheDevLogger,
    get_dev_log,
    Thread,
    List,
    os,
    sys,
)


class OsUtil:
    time_out = 3600
    process: subprocess.Popen = None

    def __init__(self, fun_name: str, error_exit_flag=True):
        self.fun_name = fun_name.replace("\\", "/")
        self.error_exit_flag = error_exit_flag
        self.root_path = "./"
        self.and_cmds = []

    def set_time_out(self, timeout):
        self.timeout = timeout
        return self

    def set_py_venv(self, env_path):
        local_exec = sys.executable.replace("\\", "/")
        if env_path in local_exec:
            return
        if not File(env_path).exists():
            OsUtil("python").run("-m", "venv", env_path)
        if os.name == "nt":
            cmd = f"{env_path}/Scripts/Activate.ps1"
        else:
            cmd = f"source {env_path}/bin/activate"
        self.logger.info(f"请用  {cmd} 进入虚拟环境执行 {local_exec}")

    def check_output(self, cmd: List[str], env=None):
        cmds = " ".join(cmd)
        self.logger.info(f"{self.root_path}->{cmds}")
        param = dict()
        param.update(self.get_std())

        use_shell = os.name == "nt"

        try:
            self.process = subprocess.Popen(
                cmd,
                shell=use_shell,
                text=True,
                cwd=self.root_path,
                env=env,
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
            self.info(msg[:20] + "..." + msg[-20:] + cmd)

    _logger: TheDevLogger = None

    def set_logger(self, logger):
        if isinstance(logger, str):
            logger = get_dev_log(logger)
        self._logger: TheDevLogger = logger
        return self

    @property
    def logger(self):
        if self._logger is None:
            self._logger = get_dev_log(f"data/log/os/{self.fun_name}.log")
        return self._logger

    def get_std(self):
        return dict(
            stderr=self.logger.get_writer(),
            stdout=self.logger.get_writer(),
        )

    def set_env(self, root):
        self.root_path: str = root
        return self

    def get_cmd(self, args, kw: dict):
        ret: List[str] = [self.fun_name] + list(args)
        for k, v in kw.items():
            ret.extend([k, v])
        return ret

    def popen(self, *args, **kw) -> subprocess.Popen:
        cmd = self.get_cmd(args, kw)
        kw.setdefault("stdout", subprocess.PIPE)
        kw.setdefault("stderr", subprocess.STDOUT)
        kw.setdefault("stdin", subprocess.PIPE)
        kw.setdefault("text", True)
        self.process = subprocess.Popen(cmd, **kw)
        return self.process

    def popen_output(self, *args, timeout=60, env=None, **kw) -> str:
        cmd = self.get_cmd(args, kw)
        statu, stdout, stderror = self.check_output(cmd, env=env)
        if statu:
            return stdout.strip()
        return ""

    def run(self, *args, env=None, **kw):
        return self.check_output(self.get_cmd(args, kw), env=env)

    def start(self, *args, **kw):
        Thread(target=self.run, args=args, kwargs=kw).start()
        return self

    def stop(self):
        if self.process:
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
