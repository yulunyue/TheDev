from common.algo.search.param import Params
from common.algo.search.state import Action
from common.algo.search.algo import Algo
from typing import List
import numpy as np


class Gene:
    def __init__(self):
        pass

    def load(self, players_fun, env_init_fun):
        self.players_fun = players_fun
        self.env_init_fun = env_init_fun
        return self

    def tournament_selection(self, tournament_size=5):
        competitors: List[Params] = np.random.choice(self.population, tournament_size)
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

    def evaluate_fitness(self, gene: Params, opponents: List[Params], num_games=20):
        wins = 0
        for op_gene in opponents:
            for _ in range(num_games):
                result1 = self.simulate_match(gene, op_gene, 0)
                result2 = self.simulate_match(gene, op_gene, 1)
                wins += result1 + result2
        return wins / (len(op_gene) * num_games * 2)

    def simulate_match(self, gene: Params, op_gene: Params, cur_player=0):
        action: Action = self.env_init_fun()
        ais: List[Algo] = [self.players_fun(gene), self.players_fun(op_gene)]
        while action.dst.done < 0:
            ais[cur_player].search(action)
            if action.dst.best_action is None:
                action.dst.debug()
                raise Exception("todo")
            action = action.dst.best_action
            cur_player = 1 - cur_player
        if action.dst.done == 0:
            return 0.5
        if action.dst.done == 1:
            return 1
        return 0

    def run(self, param: Params, generations=100, pop_size=50):
        self.population: List[Params] = self.initialize_population(param, pop_size)

        for i in range(generations):

            for gene in self.population:
                gene.score = self.evaluate_fitness(
                    gene, np.random.choice(self.population, 5)
                )
            self.population.sort(key=lambda a: -a.score)
            if i == generations - 1:
                return self.population[0]
            new_pops = self.population[: int(pop_size * 0.1)]
            while len(new_pops) < pop_size:
                p1 = self.tournament_selection(self.population)
                p2 = self.tournament_selection(self.population)
                c = self.crossover(p1, p2)
                new_pops.append(self.mutate(c))
            self.population = new_pops
