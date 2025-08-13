from common.algo.export import AlphaBateSearch, RandomAlgo
from .constant import TcEnum


class Pm:
    bl9 = AlphaBateSearch("bl10").load(10).set_params(TcEnum())
    rd1 = RandomAlgo("rd1").load()
