from common.util.export import File, logger, time
from .system import System


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
        """检查进程是否运行（跨平台）"""
        pid = self.get_pid()
        if pid is None:
            return False
        name = System.find_process_info(pid)
        return name != ""

    def start_unique(self, pid: int = None) -> bool:
        if self.is_running():
            System.kill(self.get_pid())
        else:
            self.clear()
        if pid is None:
            pid = System.getpid()
        self.set_pid(pid)
        return True

    def clear(self):
        if self.pid_file.exists():
            self.pid_file.remove()

    def start_process(self, cmd: list, cwd: str = None, log_file: str = None) -> int:
        self.start_unique()
        proc = System.popen(cmd)
        self.set_pid(proc.pid)
        logger.info(
            f"ProcessLock[{self.name}] started: {System.find_process_info(proc.pid)}"
        )
        return proc.pid
