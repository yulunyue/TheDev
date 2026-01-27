import random
from common.util.export import (
    logger,
    File,
    json_dumps,
    defaultdict,
    math,
    List,
    Dict,
    Tuple,
    dict_to_str,
)
from .action import Action

inf = float("inf")


class State:
    NO_WIN = -1
    FIRST_WIN = 1
    SECONEND_WIN = 2
    MAN2 = "MAN2"
    MAN1 = "MAN1"
    name = "state"
    parent: "State" = None
    done = False
    STATE_STORE: Dict[str, "State"] = None
    actions: List[Action] = None
    data = None
    best_action: Action = None
    extra = None
    mode = ""

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
    def new(cls, state):
        if cls.STATE_STORE is None:
            cls.STATE_STORE = dict()
        if state not in cls.STATE_STORE:
            cls.STATE_STORE[state] = cls(state)
        return cls.STATE_STORE[state]

    def get_done(self):
        return self.done

    def do_action(self, a: Action):
        return a.do().get_dst()

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

    def to_str(self, algo=None):
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

    def get_children(self):
        return self.get_sort_actions()

    def dfs(self, call, max_depth=15, call_pos="pre"):
        def util(n: State, depth=0, action: Action = None):
            if depth > max_depth:
                logger.warning(f"stack over {max_depth}")
                return
            if call_pos == "pre":
                call(n, depth, action)
            if n is None:
                return
            actions = n.get_children()
            half = len(actions) // 2
            for a in actions[:half]:
                util(a.dst, depth + 1, a)
            if call_pos == "mid":
                call(n, depth, action)
            for a in actions[half:]:
                util(a.dst, depth + 1, a)
            if call_pos == "after":
                call(n, depth, action)

        util(self, 0, None)

    def print_tree(self):
        ans = []

        def util(n: State, depth, action: Action):
            acs = ""
            if action is not None:
                info = dict(a=action.action)
                if action.reward is not None:
                    info["r"] = action.reward
                if action.src.state:
                    info["s"] = action.src.state
                acs = dict_to_str(**info)
            dst = "TODO"
            if n is not None:
                dst = n.show_titles()
            s = f'{"  " * depth}{acs}: {dst}'
            ans.append(s)

        self.dfs(util, call_pos="pre")
        return "\n".join(["---"] + ans + ["---"])

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

    def to_json(self):
        return dict(done=self.done)

    def show_titles(self):
        return dict_to_str(**self.to_json())

    def show_body(self, info, algo=None):
        datas = [self.show_titles()] + self.to_str(algo=algo)
        if self.data:
            for k, v in self.data.items():
                datas.append(f"{k}:{v}")
        if isinstance(info, list):
            datas.extend(info)
        elif info:
            datas.append(str(info))
        return datas

    def show(self, info=None, fp=None, algo=None):
        body = self.show_body(info, algo=algo)
        head = f"-----{self.title}-----"
        ret = "\n".join([head] + body + ["-" * len(head)])
        if fp:
            File(f"data/log/{fp}.log").write_file(ret)
        return ret

    @property
    def title(self):
        return str(self.state)

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

    def get_win_player(self, *args, **kw):
        return self.done - 1

    def get_next(self, *args):
        dst = self
        for a in args:
            dst = dst.get_action(a).do().get_dst()
        return dst
