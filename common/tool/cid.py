from common.util.fp import File
import os
import sys
import subprocess
PORT=8888
cron_path='/etc/crontab'

con_cmd='*/5 * * * * python3 '
def install():
    File(cron_path)

def check():
    s2=os.popen(f'netstat -nltp | grep {PORT}').read()
    restart_cmd=f'sh {__file__}'
    if s2:
        print(f'port:{PORT} check ok')
    else:
        print(f'port:{PORT} check fail restart')
        print(__name__,__file__)