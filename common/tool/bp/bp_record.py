from common.util.export import get_log, logger


class BpRecord:
    def record(self, method, node):
        logger.map(key=node.key, method=method)
