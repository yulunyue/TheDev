from common.algo.export import AbDev as AlphaBateSearch, Algo


class Pm:
    bl1 = AlphaBateSearch("bl1").load(1)
    bl2 = AlphaBateSearch("bl2").load(2)
    bl3 = AlphaBateSearch("bl3").load(3)
    bl4 = AlphaBateSearch("bl4").load(4)
    bl5 = AlphaBateSearch("bl5").load(5)
    bl6 = AlphaBateSearch("bl6").load(6)
    ab1 = AlphaBateSearch("ab1").load(1, AlphaBateSearch.AB_TYPE)
    ab2 = AlphaBateSearch("ab2").load(2, AlphaBateSearch.AB_TYPE)
    ab3 = AlphaBateSearch("ab3").load(3, AlphaBateSearch.AB_TYPE)
    ab4 = AlphaBateSearch("ab4").load(4, AlphaBateSearch.AB_TYPE)
    ab5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE)
    ab6 = AlphaBateSearch("ab6").load(6, AlphaBateSearch.AB_TYPE)  # 基线

    def all(self):
        ret = []
        for name in dir(self):
            if name.startswith("_"):
                continue
            v = getattr(self, name)
            if isinstance(v, Algo):
                ret.append(v)
        return ret


PM = Pm()
