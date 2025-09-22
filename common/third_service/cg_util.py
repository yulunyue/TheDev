from common.service.export import Api
from common.util.export import File, List, logger, get_log
from common.algo.export import Algo, State
import json


class CGFrames:
    def load(
        self,
        stdout="",
        stderr=None,
        agentId=None,
        summary="",
        gameInformation=None,
        **kw,
    ) -> "CGFrames":
        self.stdout = stdout[:-1]
        self.summary = summary.replace("\n", ",")
        self.gameInformation = gameInformation
        self.agent_id = agentId
        self.stderr = dict()
        if stderr:
            self.stderr.update(json.loads(stderr[:-1]))
        return self

    def __repr__(self):
        return f"out:{self.stdout} error:{self.stderr}"


def uu(name):
    return f"data/cg/{name}"


def ss(name):
    return uu(name + ".json")


class CodingGame(Api):

    def __init__(self, game_name):
        super().__init__()
        self.game_name = game_name

    def get_timeout(self):
        return 100

    @property
    def name(self):
        return "CodingGame"

    def execute(self, file_path, game_id, key=None, data=None, play_type="play"):
        code = open(file_path, "r", encoding="utf-8").read()
        info = dict(code=code, programmingLanguageId="Python3")
        if key:
            info[key] = data
        player_data = [game_id, info]
        if play_type == "submit":
            player_data.append(None)
        ret = self.post(f"/services/TestSession/{play_type}", player_data)
        File(ss(self.game_name + "/" + play_type)).write_file(ret)

    def submit(self, file_path, game_id):
        return self.execute(file_path, game_id, play_type="submit")

    def get_endpoint(self):
        return "www.codingame.com"

    def solve(self, file_path, game_id, text_idx=1):
        return self.execute(
            file_path, game_id, "multipleLanguages", dict(testIndex=text_idx)
        )

    def pk(self, path, game_id, agentsIds):
        ret = self.execute(
            path,
            game_id,
            "multi",
            dict(agentsIds=agentsIds, gameOptions=None, isSoloLeague=False),
        )
        return ret

    def get_cg_frames(self, name="play", filter=None) -> List[CGFrames]:
        data = File(ss(self.game_name + "/" + name)).read_file()
        ret = []
        for d in data["frames"]:
            if filter and filter(d):
                continue
            fr = CGFrames().load(**d)
            ret.append(fr)
        return ret

    def get_cg_frames_stderror(self, name="play") -> List[CGFrames]:
        return self.get_cg_frames(name, filter=lambda a: a.get("stderr") is None)

    def replay(self, state, algo: Algo):
        s: State = state
        self.logger.debug(s.show())
        from common.third_util.echarts import EChart

        last_s = None
        e = EChart()
        e.add_data(s.get_data())
        for i, f in enumerate(self.get_cg_frames()):
            if not f.stdout:
                continue
            # for k, v in f.stderr.items():
            #     self.log(f"{k} :{v}")
            if hasattr(s, "check_cg") and f.stderr:
                s.check_cg(**f.stderr, last_state=last_s)
            a = s.get_action(f.stdout)
            b = algo.search(s)
            b_action = b.action if b else None
            self.logger.debug(
                f"----[turn:{i}, cg_action:{a.action}, local_action:{b_action}, sm_{s.player_id}{a.action==b_action}]----"
            )
            last_s = s
            s = a.get_dst()
            if s:
                self.logger.debug(s.show())
                e.add_data(s.get_data())

        e.draw_lines().save(uu(f"{self.game_name}/replay.html"))

    @property
    def logger(self):
        return get_log(uu(f"{self.game_name}/replay.log"))
