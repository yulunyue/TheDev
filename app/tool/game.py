from ..yly.envs.game.c5.db import Bd
from common.tool.export import FontSearch
from common.util.export import IO_MANAGE, ApiBase


class F5Chess(ApiBase):
    def get_user(self, **kw):
        return FontSearch().add_node(IO_MANAGE.io_map.keys())

    def get_algo(self, **kw):
        return FontSearch()

    def fight(self):
        pass

    def calc(self):
        pass
