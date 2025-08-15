from common.algo.export import AlphaBateSearch, RandomAlgo, Td0
from .constant import TcEnum


class Pm:
    bl1 = AlphaBateSearch("bl1").load(1).set_params(TcEnum())
    bl2 = AlphaBateSearch("bl2").load(2).set_params(TcEnum())
    bl10 = AlphaBateSearch("bl10").load(10).set_params(TcEnum())
    rd1 = RandomAlgo("rd1").load()
    td0 = Td0("td0").load()
    td1 = Td0("td1").load()
