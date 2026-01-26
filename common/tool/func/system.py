from ..os_util import OsUtil
import re


class System:
    @classmethod
    def check_port_with_netstat(cls, port):
        statu, result, stderror = OsUtil("netstat").run("-ano")
        # 查找端口
        pattern = rf":{port}\s+"
        for line in result.split("\n"):
            if re.search(pattern, line):
                return line.strip().split(" ")
        return ""

    @classmethod
    def check_port(cls, port):
        return cls.check_port_with_netstat(port)
