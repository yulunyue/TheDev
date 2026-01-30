def floyd(dis: dict, keys):
    for k in keys:
        for i in keys:
            for j in keys:
                c = dis[i, k] + dis[k, j]
                if c < dis[i, j]:
                    dis[i, j] = c
