from common.service.export import Api
from common.util.export import File, List
import json


class CGFrames:
    def load(self, stdout, stderr=None, **kw):
        self.stdout = stdout[:-1]
        self.stderr = dict()
        if stderr:
            self.stderr.update(json.loads(stderr[:-1]))
        return self


class CodingGame(Api):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def get_local_path(self, name):
        return f"data/cg/{self.name}/{name}"

    def execute(self, file_path, game_id, key, data):
        code = open(file_path, "r", encoding="utf-8").read()
        info = dict(code=code, programmingLanguageId="Python3")
        info[key] = data
        player_data = [game_id, info]
        ret = self.post("/services/TestSession/play", player_data)
        return ret

    def get_endpoint(self):
        return "www.codingame.com"

    def solve(self, file_path, game_id):
        return self.execute(file_path, game_id, "multipleLanguages", dict(testIndex=3))

    def pk(self, path, game_id, agentsIds):
        ret = self.execute(
            path,
            game_id,
            "multi",
            dict(agentsIds=agentsIds, gameOptions=None, isSoloLeague=False),
        )
        File(self.get_local_path("play.json")).write_file(ret)
        return ret

    def get_replay_json(self) -> List[CGFrames]:
        data = File(self.get_local_path("play.json")).read_file()
        ret = []
        for d in data["frames"]:
            if "stdout" not in d:
                continue
            ret.append(CGFrames().load(**d))
        return ret
