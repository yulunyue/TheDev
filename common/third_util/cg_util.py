from common.service.export import Api
import sys
import json


class CodingGame(Api):
    def __init__(self, name):
        self.name = name
        super().__init__()

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

    def pk(self, file_path, game_id, agentsIds):
        return self.execute(
            file_path,
            game_id,
            "multi",
            dict(agentsIds=agentsIds, gameOptions=None, isSoloLeague=False),
        )


if __name__ == "__main__":
    CodingGame().run(sys.argv[1])
