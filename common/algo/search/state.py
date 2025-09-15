import random
from common.util.export import logger, json_dumps, defaultdict, math, List, Dict, Tuple
from .param import Params, Param

inf = float("inf")


class Action:
    check_info = None
    reward = 0
    regret = 0
    depth = 0

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: MctsState = src
        self.dst: MctsState = dst
        self.data = dict()

    def get_regret(self):
        return self.regret

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


class PAction(Action):
    dst = None

    def __init__(self, src, action):
        self.src: State = src
        self.action = action
        self.dst_p = dict()
        self.max_p = 0
        self.data = dict()

    def add_dst(self, state: "State", p):
        if state.state in self.dst_p:
            return
        self.dst_p[state.state] = [state, p]
        self.max_p += p

    def get_dst(self):
        a = random.random() * self.max_p
        for s, p in self.dst_p.values():
            if a <= p:
                return s
            a -= p


class State:
    name = "state"
    parent: "State" = None
    done = None
    STATE_STORE: Dict[str, "State"] = None
    sort_reward = None
    reward = None

    def __init__(self, state=None, player_id=0, depth=0) -> None:
        self.state = state
        self.depth = depth
        self.data = dict()
        self.player_id = player_id
        self.best_action: Action = None
        self.actions: Dict[str, Action] = None

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self

    @classmethod
    def new(cls, state=None, **kw):
        if cls.STATE_STORE is None:
            cls.STATE_STORE = dict()
        if state not in cls.STATE_STORE:
            cls.STATE_STORE[state] = cls(state, **kw)
        return cls.STATE_STORE[state]

    def get_done(self):
        return self.done

    def do_action(self, a: Action):
        return a.dst

    def action_size(self):
        raise Exception("tood")

    def set_best_action(self, a: Action):
        self.best_action = a
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
            actions = s.get_actions()
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

    def get_actions(self, depth=1, **kw) -> Dict[str, Action]:
        if self.actions is not None:
            return self.actions
        self.actions = self.make_actions()
        return self.actions

    def make_actions(self):
        raise Exception("todo")

    def get_random_action(self) -> Action:
        actions = self.get_sort_actions()
        return actions[random.randint(0, len(actions) - 1)]

    def to_str(self):
        return ""

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

    def dfs(self, max_depth=-1):

        DONE_S = "done"

        def dfs(s: State, depth):
            actions = s.get_sort_actions()
            if s.get_done() is not None or depth == max_depth or not actions:
                return s.set_value(DONE_S, s.get_done())
            ct = defaultdict(int)
            for a in actions:
                dst = a.get_dst()
                done = dfs(dst, depth + 1)
                if done == s.player_id:
                    return s.set_value(DONE_S, done)
                ct[done] += 1
            if ct[1 - s.player_id] == len(actions):
                return s.set_value(DONE_S, 1 - s.player_id)
            if ct[None]:
                return s.set_value(DONE_S, None)
            return s.set_value(DONE_S, -1)

        def dfs1(s: State, depth, stacks):
            actions = s.get_sort_actions()
            if depth == max_depth or not actions:
                return
            if s.get_done() is not None:
                return
            for a in actions:
                dst = a.get_dst()
                if dst.data.get(DONE_S) != s.data[DONE_S]:
                    continue
                dfs1(dst, depth + 1, stacks + [str(a.action)])

        dfs(self, 0)
        dfs1(self, 0, [])

    def get_reward(self, actions: List[Action] = None, params: Params = None) -> int:
        """
        绝对优势 >0 表示先手优势 <0 表示后手优势
        """
        return self.reward

    def get_max_action_reward(self):
        reward = -inf
        for a in self.get_actions().values():
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

    def show(self, info="", title=""):
        datas = [
            f"done:{self.get_done()}, depth:{self.depth}, player:{self.player_id}, reward:{self.reward}",
            self.to_str(),
        ]
        if self.data:
            datas.append(f"data:{self.data}")
        if info:
            datas.append(info)
        if isinstance(self.state, int):
            mask = "%s:%x" % (title, self.state)
        else:
            mask = f"{title}:{self.state}"
        mask_max_len = 60
        if len(mask) > mask_max_len:
            mask_max_len = len(mask) + 8
        margin = (mask_max_len - len(mask)) // 2
        return f"\n".join(
            ["-" * margin + mask + "-" * margin] + datas + ["-" * mask_max_len]
        )

    def get_win_player(self, rewards, player_idx, *args, **kw):
        reward = self.get_reward()
        if reward == 0:
            return -1
        if reward > 0:
            return 0
        return 1

    def get_self_reward(self, **kw):
        r = self.get_reward()
        if (
            self.player_id == 0
        ):  # Player1 回合结束，轮到Player0 走，返回对于Player1的价值 取反
            return -r
        return r

    sort_actions: List[Action] = None

    def get_sort_actions(self, **kw):
        if self.sort_actions is None:
            self.sort_actions = list(self.get_actions().values())
        return self.sort_actions

    def get_data(self):
        return dict(reward=self.reward)


class MctsState(State):
    visite_num = 0
    visite_score = 0

    def __init__(self, state=None, player_id=0, depth=0):
        super().__init__(state, player_id, depth)
        self.expand_actions: List[Action] = []
        self.need_expand_actions: List[Action] = None

    def get_need_expand_actions(self):
        if self.need_expand_actions is not None:
            return self.need_expand_actions
        self.need_expand_actions = list(self.get_actions().values())
        return self.need_expand_actions

    def is_fully_expanded(self):
        return len(self.get_need_expand_actions()) == 0

    def get_uct_best_child(self, exploration_param=1.4):
        best_score = -float("inf")
        best_child = None
        for action in self.expand_actions:
            child: MctsState = action.get_dst()
            # UCT公式
            exploit = child.visite_score / child.visite_num
            explore = exploration_param * math.sqrt(
                math.log(self.visite_num) / child.visite_num
            )
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        action = self.get_need_expand_actions().pop()
        self.expand_actions.append(action)
        return action.get_dst()

    def show(self, info="", title=""):
        if self.visite_num:
            s += f"vt_num:{self.visite_num}; vt_score:{self.visite_score}; need_expand:{len(self.get_need_expand_actions())}; expand_actions:{len(self.expand_actions)}"

        return super().show(info=info, title=title)
