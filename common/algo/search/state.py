import random
from common.util.export import logger, json_dumps, defaultdict, math, List, Dict, Tuple


inf = float("inf")


class Action:
    check_info = None
    reward = None

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.data = dict()

    @property
    def title(self):
        return self.action

    @property
    def key(self):
        return f"{self.src.state}->{self.action}"

    def get_dst(self):
        return self.dst

    def get_data(self, key, default_value):
        return self.data.get(key, default_value)

    def set_data(self, **kw):
        self.data.update(kw)
        return self

    p = None

    def set_p(self, p):
        self.p = p
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    def get_reward(self, **kwargs):
        return self.reward

    def get_src_reward(self, **kw):
        pass

    def show(self, msg=None):
        ret = f"src:{self.src.state}, dst:{self.dst.state}, action:{self.action}"
        if self.data:
            ret += f", data:{self.data}"
        if msg:
            ret += f", msg:{msg}"
        if self.reward is not None and self.reward > 0:
            ret += f", rwin:{self.reward}"
        elif self.reward is not None and self.reward < 0:
            ret += f", rlos:{self.reward}"
        return ret

    def show_best_actions(self):
        a = self
        ret = []
        while a:
            ret.append(a.show())
            ret.append(a.get_dst().show())
            a = a.get_dst().get_action()
        return "\n".join(ret)

    def do(self):
        """ """
        pass

    def get_dqn_network_params(self, actions: List["Action"]):
        """
        rewards, dones, q_values, max_next_q_values
        """
        pass


class State:
    NO_WIN = -1
    FIRST_WIN = 1
    SECONEND_WIN = 2
    name = "state"
    parent: "State" = None
    done = None
    STATE_STORE: Dict[str, "State"] = dict()
    actions: List[Action] = None
    data = None
    best_action: Action = None

    def __init__(self, state=None, player_id=0, depth=0) -> None:
        self.state: int = state
        self.depth = depth
        self.player_id = player_id  # 下一回合的执行者

    def init_data(self):
        self.data = dict()
        return self

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self

    @classmethod
    def new(cls, state=None, **kw):
        if state not in cls.STATE_STORE:
            cls.STATE_STORE[state] = cls(state, **kw)
        return cls.STATE_STORE[state]

    def get_done(self):
        return self.done

    def do_action(self, a: Action):
        return a.get_dst()

    def action_size(self):
        raise Exception("tood")

    def set_best_action(self, a: Action):
        self.best_action = a
        return self

    def set_best_state(self, a: "State"):
        self.best_state = a
        return self

    def set_depth(self, depth):
        self.depth = depth
        return self

    def set_done(self, done):
        self.done = done
        return self

    def set_actions(self, actions):
        self.actions = actions
        return self

    def reset(self):
        return self

    @classmethod
    def reset_env(cls):
        pass

    def get_action(self, actions) -> Action:
        if not isinstance(actions, list):
            actions = [actions]
        s = self
        for a in actions:
            actions = {a.action: a for a in s.get_sort_actions()}
            if a not in actions:
                raise Exception(a, list(actions.keys()), self.state)
            ret = actions[a]
            s = ret.get_dst()
        return ret

    def get_best_actions(self) -> List["Action"]:
        p = self
        ret: List[Action] = []
        while p and not p.get_done():
            a = p.get_best_action()
            if not a:
                break
            ret.append(a)
            p = a.get_dst()
        return ret

    def get_best_action(self):
        return self.best_action

    def make_actions(self):
        raise Exception("todo")

    def get_random_action(self) -> Action:
        actions = self.get_sort_actions()
        idx = random.randint(0, len(actions) - 1)
        return actions[idx]

    def random_step(self, n):
        ret = self
        for _ in range(n):
            if ret.game_over():
                return ret
            ret = ret.get_random_action().get_dst()
        return ret

    def to_str(self):
        return []

    def bfs(self, max_depth=15) -> Dict[str, Tuple[List[Action], "State"]]:
        ret = {self.state: [[], self]}
        q = [self]
        while q and max_depth != -1:
            t = q
            q = []
            for s in t:
                actions = ret[s.state][0]
                for a in s.get_sort_actions():
                    d = a.get_dst()
                    if d.state in ret:
                        continue
                    ret[d.state] = [actions + [a], d]
                    q.append(d)
            max_depth -= 1
        return ret

    def dfs(self, call, max_depth=15, call_pos="pre"):
        def util(n: State, depth=0, action: Action = None):
            if depth > max_depth:
                logger.warning(f"stack over {max_depth}")
                return
            if call_pos == "pre":
                call(n, depth, action)
            actions = n.get_sort_actions()
            half = len(actions) // 2
            for a in actions[:half]:
                util(a.get_dst(), depth + 1, a)
            if call_pos == "mid":
                call(n, depth, action)
            for a in actions[half:]:
                util(a.get_dst(), depth + 1, a)
            if call_pos == "after":
                call(n, depth, action)

        util(self, 0, None)

    def print_tree(self):
        ans = []

        def util(n: State, depth, action: Action):
            key = ""
            if action is not None:
                key = action.key
            s = f'{"  " * depth}{key}: {n.show_titles()}'
            ans.append(s)

        self.dfs(util, call_pos="pre")
        return "\n".join(ans)

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_sort_actions():
            ar = a.get_reward()
            if ar > reward:
                reward = ar
        return reward

    def set_data(self, **kw):
        self.data.update(kw)
        return self

    def set_value(self, k, v):
        self.data[k] = v
        return self.data[k]

    def show_titles(self):
        return "todo"

    def show_body(self, info):
        datas = [self.show_titles()] + self.to_str()
        if self.data:
            for k, v in self.data.items():
                datas.append(f"{k}:{v}")
        if isinstance(info, list):
            datas.extend(info)
        elif info:
            datas.append(str(info))
        return datas

    def show(self, info=None):
        body = self.show_body(info)
        head = f"--{self.title}--"
        return "\n".join([head] + body + ["-" * len(head)])

    @property
    def title(self):
        return str(self.state)

    def get_win_player(self, *args, **kw):
        return self.done

    def get_sort_actions(self, **kw):
        if self.actions is None:
            self.actions = self.make_actions()
        return self.actions

    def get_data(self):
        return self.data

    def do_move(self, action: Action):
        return action.get_dst()

    def game_over(self):
        if self.done is None or self.done == False:
            return False
        return True

    @classmethod
    def get_root(cls):
        return cls.new()

    def draw_graph(self):
        from common.third_util.draw import Draw

        states = self.bfs().values()
        ret = dict()
        for _, s in states:
            ret[s.title] = []
            for a in s.get_sort_actions():
                ret[s.title].append([a.title, a.get_dst().title])
        Draw().draw_graph(ret).save(f"data/state/{self.name}.svg")


class AbState(State):

    def load_ab(self, search_depth=0, alpha=-inf, bate=inf):
        self.search_depth = search_depth
        self.child_index = 0
        self.alpha = alpha
        self.bate = bate
        return self
