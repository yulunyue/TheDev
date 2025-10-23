from common.util.export import TheDevLoger


class LogHelp:
    logger: TheDevLoger
    fz_num = 0

    def debug(self, msg):
        self.logger.debug(msg)


logger = LogHelp()
