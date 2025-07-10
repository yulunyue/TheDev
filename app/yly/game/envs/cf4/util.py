from common.algo.search.alphabate_search import AlphaBateSearch


class Pm:
    ab1 = AlphaBateSearch().load(1).set_name("ab1")
    bl1 = AlphaBateSearch().load(2, search_type=AlphaBateSearch.BR_TYPE).set_name("bl1")
