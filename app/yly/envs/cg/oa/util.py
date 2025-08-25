from common.algo.export import AbDev as AlphaBateSearch


class PM:
    bl1 = AlphaBateSearch("bl1").load(1)
    bl2 = AlphaBateSearch("bl2").load(2)
    bl3 = AlphaBateSearch("bl3").load(3)
    bl4 = AlphaBateSearch("bl4").load(4)
    bl5 = AlphaBateSearch("bl5").load(5)
    bl6 = AlphaBateSearch("bl6").load(6)
    ab1 = AlphaBateSearch("ab1").load(1, AlphaBateSearch.AB_TYPE)
    ab3 = AlphaBateSearch("ab3").load(3, AlphaBateSearch.AB_TYPE)
    ab4 = AlphaBateSearch("ab4").load(4, AlphaBateSearch.AB_TYPE)
    ab5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE)  # 112
