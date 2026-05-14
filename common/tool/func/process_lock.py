"""
进程锁管理器
用于确保进程唯一性，支持启动前检查旧进程并自动关闭

使用示例：
    # 方式1：简单使用（推荐）
    lock = ProcessLock("qt")
    if lock.start_unique():
        lock.set_pid(os.getpid())
    
    # 方式2：手动控制
    lock = ProcessLock("backend")
    if lock.is_running():
        lock.kill_old()
    lock.set_pid(os.getpid())
    
    # 方式3：启动子进程并自动记录PID
    lock = ProcessLock("frontend")
    proc = lock.start_process(["npm", "start"], cwd="font")
"""

from common.util.export import File, logger, os, time
import subprocess


class ProcessLock:
    PID_DIR = "data/proc"

    def __init__(self, name: str):
        self.name = name
        self.pid_file = File(f"{self.PID_DIR}/{name}.pid")
        self.pid_file.parent().make_dir_if_not_exist(True)

    def get_pid(self) -> int | None:
        if self.pid_file.exists():
            try:
                content = self.pid_file.read_file()
                if isinstance(content, str):
                    content = content.strip()
                if content:
                    return int(content)
            except Exception:
                pass
        return None

    def set_pid(self, pid: int):
        self.pid_file.write_file(str(pid))
        logger.info(f"ProcessLock[{self.name}] set PID={pid}")

    def is_running(self) -> bool:
        pid = self.get_pid()
        if pid is None:
            return False
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except Exception:
            return False

    def kill_old(self) -> bool:
        pid = self.get_pid()
        if pid is None:
            return True
        try:
            logger.info(f"ProcessLock[{self.name}] kill old PID={pid}")
            os.kill(pid, 9)
            time.sleep(0.5)
            self.clear()
            return True
        except ProcessLookupError:
            self.clear()
            return True
        except Exception as e:
            logger.error(f"ProcessLock[{self.name}] kill failed: {e}")
            return False

    def start_unique(self, pid: int = None) -> bool:
        if self.is_running():
            if not self.kill_old():
                return False
        else:
            self.clear()
        if pid is None:
            pid = os.getpid()
        self.set_pid(pid)
        return True

    def clear(self):
        if self.pid_file.exists():
            self.pid_file.remove()

    def start_process(self, cmd: list, cwd: str = None, log_file: str = None) -> int:
        self.start_unique()
        kwargs = {}
        if cwd:
            kwargs["cwd"] = cwd
        if log_file:
            log_f = File(log_file)
            log_f.parent().make_dir_if_not_exist(True)
            kwargs["stdout"] = open(log_f.get_abs_path(), "w")
            kwargs["stderr"] = subprocess.STDOUT
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, **kwargs)
        return proc.pid