from .api import ApiAlgo


class PM:
    api = ApiAlgo().load()


def get_player(s):
    if isinstance(s, str):
        return getattr(PM, s)
    return s
