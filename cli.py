from common.tool.export import OsUtil, System
import os

pid = System.get_pid_by_port(10000)
OsUtil("kill").run("-9", pid)
OsUtil("python").system("main.py", "http", "2>&1", "&")
