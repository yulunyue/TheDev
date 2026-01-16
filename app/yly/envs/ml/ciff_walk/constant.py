class C:
    ACTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    ACS = ["^", "v", "<", ">"]
    ncol = 12
    nrow = 4
    INIT_SATTE = 36

    def to_matrix(p, tp=None):
        ret = []
        for i in range(C.nrow):
            ret.append([])
            for j in range(C.ncol):
                k = i * C.ncol + j
                if isinstance(p, Algo):
                    s = CfState.new(k)
                    v = "N"
                    if not s.game_over():
                        if tp is None:
                            v = p.take_action(s).action
                        else:
                            v = [p.q.get(a.key) for a in s.get_sort_actions()]
                else:
                    v = p.get(k, "")
                if isinstance(v, float):
                    v = "%.3f" % (v)
                elif isinstance(v, list):
                    v = ",".join(["%.2f" % (s) for s in v])
                elif isinstance(v, dict):
                    v = "".join(C.ACS[k] if v[k] != 0 else "" for k in v)
                elif isinstance(v, int):
                    v = C.ACS[v]
                ret[-1].append(v)
        p = PtTable().load_from_matrix(ret)
        return p.show()
