from ..os_util import OsUtil
from common.util.export import List, os, re


def find_port(result, port):
    # 查找端口
    pattern = rf":{port}\s+"
    for line in result.split("\n"):
        if re.search(pattern, line):
            return line.strip().split(" ")
    return ""


class System:
    @classmethod
    def get_pid_by_port_windows(cls, port):
        statu, result, stderror = OsUtil("netstat").run("-ano")
        return find_port(result, port)

    @classmethod
    def get_pid_by_port_linux(cls, port):
        statu, result, stderror = OsUtil("netstat").run("-nltp")

        return find_port(result, port)[-1].split("/")[0]

    @classmethod
    def get_pid_by_port(cls, port):
        if os.name == "nt":
            return cls.get_pid_by_port_windows(port)
        return cls.get_pid_by_port_linux(port)
