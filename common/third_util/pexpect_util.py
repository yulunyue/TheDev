import pexpect


class PexpectUtil:
    def __init__(self, cmd):
        self.ins = pexpect.spawn(cmd)
        self.time_out = 10

    def expect(self, key, next_cmd=None):
        self.ins.expect(key, timeout=self.time_out)
        if next_cmd:
            self.ins.sendline(next_cmd)
