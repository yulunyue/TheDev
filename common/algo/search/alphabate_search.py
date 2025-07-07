from common.algo.search.state import State, inf, Action
from common.algo.search.algo import Algo
from typing import List, Dict
from common.util.export import logger, defaultdict


class AlphaBateSearch(Algo):
    AB_TYPE = "alphabate"
    BR_TYPE = "brutal"

    def load(self, max_depth, use_cache=False, search_type=""):
        self.max_depth = max_depth
        self.search_type = search_type
        return super().load(use_cache=use_cache)

    def search_ab(
        self,
        state: State,
        action: Action = None,
        depth=0,
        alpha=-inf,
        bate=inf,
        player_id=None,
        **kw,
    ) -> None:
        if depth == self.max_depth:
            return action.get_reward(
                depth=depth, params=self.params, player_id=player_id
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return action.get_reward(
                depth=depth, params=self.params, player_id=player_id
            )
        for k, a in mvs.items():
            reward = self.search_ab(
                a.dst,
                action=a,
                depth=depth + 1,
                alpha=-bate,
                bate=-alpha,
                player_id=player_id,
            )
            if reward >= bate:
                alpha = bate
                state.set_best_action(a)
                break
            if reward > alpha:
                alpha = reward
                state.set_best_action(a)
        return alpha

    def search_dfs(
        self, state: State, action: Action = None, depth=0, player_id=None, **kw
    ):
        if depth == self.max_depth:
            return action.get_reward(
                depth=depth, params=self.params, player_id=player_id
            )
        mvs: Dict[str, Action] = state.get_actions(depth=depth)
        if not mvs:
            return action.get_reward(
                depth=depth, params=self.params, player_id=player_id
            )
        best_reward = -inf
        for k, a in mvs.items():
            reward = self.search_dfs(a.dst, action=a, depth=depth + 1)
            if reward > best_reward:
                state.set_best_action(a)
                best_reward = reward
        return best_reward

    def search_with_done(self, s: State):
        ret = []

        def dfs(state: State, depth=0):
            done = state.get_done()
            if done or depth == self.max_depth:
                return state.set_data("done",done)
            mvs = list(state.get_actions(depth=depth).values())
            ct = defaultdict(int)
            for a in mvs:
                done = dfs(a.dst, depth + 1)
                ct[done]+=1

            for k, value in ct.items():
                if k == state.player_id and value:
                    return state.set_data("done",k)
                elif k and ct[done] == len(mvs):
                    return state.set_data("done",k)
            return state.set_data("done",0)
        def dfs2(state:State,depth=0):
            done = state.get_done()
            if done or depth == self.max_depth:
                return
            mvs = list(state.get_actions(depth=depth).values())
            for a in mvs:
                if not a.dst.data["done"]:
                    continue
                s=f'{" "*depth}- {a}: {a.dst.data["done"]}'
                ret.append(s)
                dfs2(a.dst,depth+1)

        dfs(s)
        dfs2(s)
        # ret.reverse()
        return "\n" + "\n".join(ret)

    def search_main(self, state: State, **kw):
        if self.search_type == AlphaBateSearch.AB_TYPE:
            return self.search_ab(
                state, action=None, depth=0, player_id=state.player_id, **kw
            )
        elif self.search_type == AlphaBateSearch.BR_TYPE:
            records = self.search_with_done(state)
            state.set_data("records", records)
            return
        return self.search_dfs(
            state, action=None, depth=0, player_id=state.player_id, **kw
        )
