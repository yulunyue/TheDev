from common.algo.export import AlphaBateSearch, RandomAlgo
from .constant import TcEnum


class Pm:
    bl1 = AlphaBateSearch("bl1").load(1).set_params(TcEnum())
    bl10 = AlphaBateSearch("bl10").load(10).set_params(TcEnum())
    rd1 = RandomAlgo("rd1").load()
