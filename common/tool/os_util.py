import subprocess


class OsUtil:
    def check_output(self, cmd):
        return subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
