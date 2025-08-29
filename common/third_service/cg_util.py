from common.service.export import Api
from common.util.export import File, List, logger
from common.algo.export import Algo
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
        File(ss(play_type)).write_file(ret)

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
        data = File(ss(name)).read_file()
        ret = []
        for d in data["frames"]:
            if filter and filter(d):
                continue
            fr = CGFrames().load(**d)
            ret.append(fr)
        return ret

    def get_cg_frames_stderror(self, name="play") -> List[CGFrames]:
        return self.get_cg_frames(name, filter=lambda a: a.get("stderr") is None)

    def replay(self, state_cls, algo: Algo):
        last_f = None
        for i, f in enumerate(self.get_cg_frames()):
            self.log(f"----[turn: {i}--action: {f.stdout}]----")
            for k, v in f.stderr.items():
                self.log(f"{k} :{v}")
            s = state_cls(last_f, f)
            self.log(s)
            # a = algo.search(s)
            # self.log(a)
            last_f = f

    def log(self, msg):
        f = File(uu("replay.log")).get_writer()
        f.write(f"{msg}\n")
        f.flush()
