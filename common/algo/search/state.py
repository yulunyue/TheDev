import random
from common.util.export import logger, json_dumps, defaultdict, math, List, Dict, Tuple


inf = float("inf")


class Action:
    check_info = None
    reward = 0

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.data = dict()

    @property
    def key(self):
        return f"{self.src.state}_{self.action}"

    def get_dst(self):
        return self.dst

    def get_data(self, key, default_value):
        return self.data.get(key, default_value)

    def set_data(self, key, value):
        self.data[key] = value
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

    def show(self):
        ret = f"action: {self.action}, data:{self.data}"
        if self.reward > 0:
            ret += f", rwin: {self.reward}"
        elif self.reward < 0:
            ret += f", rlos: {self.reward}"
        return ret

    def show_best_actions(self):
        a = self
        ret = []
        while a:
            ret.append(a.show())
            ret.append(a.get_dst().show())
            a = a.get_dst().get_action()
        return "\n".join(ret)


class State:
    name = "state"
    parent: "State" = None
    done = None
    STATE_STORE: Dict[str, "State"] = dict()
    reward = None
    actions: List[Action] = None
    data = None
    best_action: Action = None

    def __init__(self, state=None, player_id=0, depth=0) -> None:
        self.state: int = state
        self.depth = depth
        self.player_id = player_id

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

    def set_reward(self, reward):
        self.reward = reward
        return self

    def set_actions(self, actions):
        self.actions = actions
        return self

    def set_next_states(self, states: List["State"]):
        return self.set_actions(
            [
                Action(self, v.state, v.set_player_id(1 - self.player_id))
                for i, v in enumerate(states)
            ]
        )

    def reset(self):
        return self

    def reset_env(self):
        return self

    def get_dst(self, actions):
        return self.get_action(actions).get_dst()

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
        return actions[random.randint(0, len(actions) - 1)]

    def to_str(self):
        return []

    def bfs(self, max_depth=-2) -> Dict[str, Tuple[List[Action], "State"]]:
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

    def dfs(self, call, max_depth=-1, call_pos="pre"):
        def util(n: State, depth=0, action: Action = None):
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

        util(self, 0, Action(None, ""))

    def print_tree(self):
        ans = []

        def util(n: State, depth, action: Action):
            s = f'{"  " * depth}{action.action}->{n.state}: {n.show_titles()}'
            ans.append(s)

        self.dfs(util, call_pos="pre")
        return "\n".join(ans)

    def get_reward(self, actions: List[Action] = None, params=None) -> int:
        """
        绝对优势 >0 表示先手优势 <0 表示后手优势
        """
        return self.reward

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_sort_actions():
            ar = a.get_self_reward()
            if ar > reward:
                reward = ar
        return reward

    def set_data(self, **kw):
        self.data.update(kw)
        return self

    def set_value(self, k, v):
        self.data[k] = v
        return self.data[k]

    header_title = ""

    def set_headers(self, s):
        self.header_title = s
        return self

    def title_show_keys(self):
        return ["p", "d", "r"]

    def show_titles(self):
        ret = []
        for k in self.title_show_keys() + [self.header_title]:
            if not k:
                continue
            if k.find("=") != -1:
                ret.append(k)
                continue
            elif k == "p":
                value = self.player_id
            elif k == "r":
                value = self.get_reward()
            elif k == "d":
                value = self.get_done()
            else:
                value = getattr(self, k)
            ret.append(f"{k}={value}")
        return "; ".join(ret)

    def show_body(self, info="", mask_max_len=50):
        datas = [self.show_titles()] + self.to_str()
        if self.data:
            for k, v in self.data.items():
                datas.append(f"{k}:{v}")
        if isinstance(info, list):
            datas.extend(info)
        elif info:
            datas.append(str(info))
        return [(d + " " * mask_max_len)[:mask_max_len] for d in datas]

    def show_array(self, info="", title="", mask_max_len=50, body=None):
        if not title:
            title = "%x" % self.state
        else:
            title = "%s:%x" % (title, self.state)
        if len(title) > mask_max_len:
            mask_max_len = len(title) + 8
        if body is None:
            body = self.show_body(info, mask_max_len)
        margin_left = (mask_max_len - len(title)) // 2
        margin_right = mask_max_len - len(title) - margin_left
        return (
            ["-" * margin_left + title + "-" * margin_right]
            + body
            + ["-" * mask_max_len]
        )

    def show(self, info="", title="", mask_max_len=40):
        return f"\n".join(self.show_array(info="", title="", mask_max_len=mask_max_len))

    def get_win_player(self, rewards, player_idx, *args, **kw):
        if self.done == 0:
            return 0
        elif self.done == 1:
            return 1
        return 2

    def get_self_reward(self, *args, **kw):
        r = self.get_reward()
        if (
            self.player_id == 0
        ):  # Player1 回合结束，轮到Player0 走，返回对于Player1的价值 取反
            return -r
        return r

    def get_sort_actions(self, **kw):
        if self.actions is None:
            self.actions = self.make_actions()
        return self.actions

    def get_data(self):
        return dict(reward=self.reward)

    def do_move(self, action: Action):
        return action.get_dst()

    @property
    def game_over(self):
        return self.done is not None


class AbState(State):

    def load_ab(self, search_depth=0, alpha=-inf, bate=inf):
        self.search_depth = search_depth
        self.child_index = 0
        self.alpha = alpha
        self.bate = bate
        return self
