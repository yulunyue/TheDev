from common.algo.export import AbDev as AlphaBateSearch


class PM:
    bl1 = AlphaBateSearch("bl1").load(1)
    bl6 = AlphaBateSearch("bl6").load(6)
    ab1 = AlphaBateSearch("ab6").load(1, AlphaBateSearch.AB_TYPE)
    ab3 = AlphaBateSearch("bl5").load(3, AlphaBateSearch.AB_TYPE)
    ab5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE)  # 基线
