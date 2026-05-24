from common.util.export import File, logger, time
from .system import System


class ProcessLock:
    PID_DIR = "data/proc"

    def __init__(self, name: str):
        self.name = name
        self.pid_file = File(f"{self.PID_DIR}/{name}.pid")
        self.pid_file.parent().make_dir_if_not_exist(True)

    def get_pid(self) -> int:
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
        logger.info(f"ProcessLock[{self.name}] set PID={pid} success")

    def is_running(self) -> bool:
        """检查进程是否运行（跨平台）"""
        pid = self.get_pid()
        if pid is None:
            return False
        name = System.find_process_info(pid)
        return name != ""

    def start_unique(self) -> int:
        old_pid = self.get_pid()
        try:
            System.kill(old_pid)
            logger.info(f"kill {old_pid} success")
        except Exception as e:
            self.clear()
            logger.info(f"kill {old_pid} fail")
        return System.getpid()

    def start(self):
        self.set_pid(self.start_unique())

    def clear(self):
        if self.pid_file.exists():
            self.pid_file.remove()

    def start_process(self, *cmd, cwd: str = None) -> int:
        self.start_unique()
        proc = System.popen(cmd, cwd=cwd)
        self.set_pid(proc.pid)
        return proc.pid
