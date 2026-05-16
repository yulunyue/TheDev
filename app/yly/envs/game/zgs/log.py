from common.util.export import TheDevLogger

class LogHelp:
    logger: TheDevLogger = None

    def set_mp(self, mp):
        self.mp = mp
        self.fz_count = 0

    def fz_num_change(self, num):
        self.fz_count += num

    def debug(self, msg):
        if self.logger is None:
            return
        self.logger.debug(msg)

    def game_over(self):
        ret = self.fz_count == 0 or self.mp.dead
        return ret


logger = LogHelp()
