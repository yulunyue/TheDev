from common.algo.search.param import Params
from common.algo.search.states.state import Action
from common.algo.search.algo import Algo
from common.util.export import get_log, logger


from typing import List
import numpy as np
import random


class Gene:
    def __init__(self):
        pass

    def load(self):
        return self

    def tournament_selection(self, tournament_size):
        competitors: List[Params] = random.sample(self.population, tournament_size)
        competitors.sort(key=lambda x: -x.score)
        return competitors[0]  # 选择锦标赛中表现最优的个体

    def crossover(self, p1: Params, p2: Params):
        def util(key):
            return (
                p1._params[key].get_value()
                if np.random.rand() < 0.5
                else p2._params[key].get_value()
            )

        return p1.new(util)

    def mutate(self, p: Params, mutation_rate=0.15):
        def util(key):
            if np.random.rand() < mutation_rate:
                return np.random.randint(
                    p._params[key].min_value, p._params[key].max_value
                )

            return p._params[key].get_value()

        return p.new(util)

    def initialize_population(self, param: Params, pop_size):
        ret = []
        for _ in range(pop_size):
            ret.append(param.new())
        return ret

    def run(
        self,
        param: Params,
        generations=2,
        pop_size=6,
        fict_size=3,
        new_rate=3,
        num_games=1,
        **kw,
    ):
        self.population: List[Params] = self.initialize_population(param, pop_size)

        for i in range(generations):
            for gene in self.population:
                gene.score = self.evaluate_fitness(
                    gene, np.random.choice(self.population, fict_size), num_games
                )
            self.population.sort(key=lambda a: -a.score)
            if i == generations - 1:
                return self.population[0]
            new_pops = self.population[:new_rate]
            while len(new_pops) < pop_size:
                p1 = self.tournament_selection(fict_size)
                p2 = self.tournament_selection(fict_size)
                c = self.crossover(p1, p2)
                new_pops.append(self.mutate(c))
            self.population = new_pops
