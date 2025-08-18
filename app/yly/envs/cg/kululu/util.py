from common.third_util.export import CGFrames, CodingGame
from common.util.export import List, File
from app.yly.envs.cg.kululu.cg import Kululu, Grid
from common.algo.export import AlphaBateSearch


class Pm:
    am1 = AlphaBateSearch("am1").load(1, search_type=AlphaBateSearch.SERACH_MAX)
