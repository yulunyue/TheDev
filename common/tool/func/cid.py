from common.util.fp import File
import os
import sys
import subprocess

PORT = 9999
cron_path = "/etc/crontab"

cron_cmd = "*/5 * * * * python3 /opt/cloud/thedev/main.py check"


def install():
    pass


def check():
    s2 = os.popen(f"netstat -nltp | grep {PORT}").read()
    if s2:
        print(s2)
        print(f"port:{PORT} check ok")
    else:
        print(f"port:{PORT} check fail restart")
        os.system("sh /opt/cloud/thedev/restart.sh")
