from common.util.export import get_log

logger = get_log("bp")


class BpRecord:
    def record(self, method, node):
        logger.map(key=node.key, method=method)
