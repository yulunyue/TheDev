from common.tool.export import OsUtil, ToolBase, GC, ProcessLock, System
from common.util.export import File, logger, md5


class SystemTool(ToolBase):
    def kill_py_port(self, port):
        pid = System.get_pid_by_port(port)
        logger.info(f"find {port} {pid}")
        if pid is None:
            return
        info = System.find_process_info(pid)
        System.kill(pid)
        logger.map(pid=pid, info=info)


if __name__ == "__main__":
    SystemTool().run()
