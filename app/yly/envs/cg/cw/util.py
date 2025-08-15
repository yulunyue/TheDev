from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from .cg import World, CgCw
from .model.constant import VE
from common.algo.search.alphabate_search import AlphaBateSearch


class Util:
    ab1 = AlphaBateSearch("ab1").load(1)
