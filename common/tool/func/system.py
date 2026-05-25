"""
系统工具类
跨平台进程查询和端口监听检测
"""

from common.util.export import logger, os
import subprocess


class System:
    """系统工具类（跨平台进程查询）"""

    @classmethod
    def get_pid_by_port(cls, port: int) -> int:
        """根据端口查找监听进程的 PID"""
        if os.name == "nt":
            return cls._get_pid_by_port_windows(port)
        return cls._get_pid_by_port_linux(port)

    @classmethod
    def getpid(cls):
        return os.getpid()

    @classmethod
    def kill(cls, pid, mode=15):
        return os.kill(pid, mode)

    @classmethod
    def _get_pid_by_port_windows(cls, port: int) -> int:
        """Windows: 使用 netstat -ano"""
        try:
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split("\n"):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.strip().split()
                    if parts:
                        return int(parts[-1])
        except Exception as e:
            logger.error(f"get_pid_by_port_windows failed: {e}")
        return None

    @classmethod
    def _get_pid_by_port_linux(cls, port: int) -> int:
        """Linux: 使用 netstat -nltp"""
        try:
            result = subprocess.run(
                ["netstat", "-nltp"], capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split("\n"):
                if f":{port}" in line:
                    for part in line.strip().split():
                        if "/" in part:
                            return int(part.split("/")[0])
        except Exception as e:
            logger.error(f"get_pid_by_port_linux failed: {e}")
        return None

    @classmethod
    def find_process_info(cls, pid: int) -> str:
        """获取进程详细信息字符串"""
        try:
            if os.name == "nt":
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = [p.strip('"') for p in lines[1].split(",")]
                    name = parts[0] if parts else "unknown"
                    mem = parts[4] if len(parts) > 4 else ""
                    return name
            else:
                result = subprocess.run(
                    ["ps", "-p", str(pid), "-o", "pid,comm,state"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = lines[1].split()
                    name = parts[1] if len(parts) > 1 else "unknown"
                    status = parts[2] if len(parts) > 2 else "unknown"
                    return f"PID: {pid} | Name: {name} | Status: {status}"
        except Exception:
            pass
        return ""

    @classmethod
    def popen(cls, cmd, cwd=None, **kw):
        if os.name == "nt":
            kw["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            kw["shell"] = True
        kw["start_new_session"] = True
        try:
            return subprocess.Popen(cmd, cwd=cwd, **kw)
        except Exception as e:
            raise Exception(cmd, cwd, kw)

    @classmethod
    def run(cls, cmd, cwd=None):
        kwargs = {}
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
        System.popen(cmd, cwd=cwd, **kwargs)
