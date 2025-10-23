from common.util.export import TheDevLoger


class LogHelp:
    logger: TheDevLoger = None
    fz_num = 0

    def debug(self, msg):
        if self.logger is None:
            return
        self.logger.debug(msg)


logger = LogHelp()
