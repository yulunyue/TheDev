from common.algo.export import AlphaBateSearch, RandomAlgo


class Pm:
    ab1 = AlphaBateSearch().load(1).set_name("ab1")
    ab2 = AlphaBateSearch().load(2).set_name("ab2")
    ab3 = AlphaBateSearch().load(3).set_name("ab3")
    ab4 = AlphaBateSearch().load(4).set_name("ab4")
    ab5 = AlphaBateSearch().load(5).set_name("ab5")
    rn = RandomAlgo().load()
