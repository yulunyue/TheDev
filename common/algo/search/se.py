import math
import random
from common.algo.search.param import Params, Param
import numpy as np


class SeOptimize:

    def load(self, match_pk_fun):
        self.match_pk_fun = match_pk_fun
        return self

    def run(self, params: Params, T0=1000, alpha=0.95, max_iter=500, **kw):
        current_params = params.clone()
        current_cost = -self.match_pk_fun(current_params, **kw)
        best_params = params.clone()
        best_cost = current_cost
        T = T0

        def util(p: Param):
            delta = random.gauss(0, T / T0)  # 温度相关扰动
            return np.clip(p.value + delta, p.min_value, p.max_value)

        for i in range(max_iter):
            # 生成邻域解
            neighbor_params = current_params.clone(util)

            # 计算新解成本
            neighbor_cost = -self.match_pk_fun(neighbor_params, **kw)

            # Metropolis准则
            delta_cost = neighbor_cost - current_cost
            if delta_cost < 0 or math.exp(-delta_cost / T) > random.random():
                current_params = neighbor_params
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best_params = current_params
                    best_cost = current_cost

            # 降温
            T *= alpha

            # 打印进度
            if i % 50 == 0:
                print(f"Iter {i}: Temp={T:.2f} Best Cost={best_cost:.4f}")

        return best_params, best_cost
