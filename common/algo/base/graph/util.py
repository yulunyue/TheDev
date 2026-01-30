from common.util.export import inf


def floyd(dis: dict, src_keys: set, dst_keys: set):
    keys = src_keys | dst_keys
    for k in keys:
        if k not in dis:
            continue
        for i in src_keys:
            if k not in dis[i]:
                continue
            for j in dst_keys:
                if j not in dis[k]:
                    continue
                c = dis[i][k] + dis[k][j]
                if c < dis[i].get(j, inf):
                    dis[i][j] = c
