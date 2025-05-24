from common.service.export import Api
from common.util.export import File


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
