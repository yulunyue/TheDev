from common.service.api import Api, StrModel
import sys
from common.util.module import Module
from common.util.log import logger
from common.util.fp import File
import json


class CodingGame(Api):

    def execute(self, file_path, game_id, key, data):
        code = open(file_path, 'r').read()
        info = dict(code=code, programmingLanguageId='Python3')
        info[key] = data
        player_data = [game_id, info]
        ret = self.post(
            '/services/TestSession/play', player_data)
        return ret
    def get_endpoint(self):
        return 'www.codingame.com'
    def solve(self, file_path, game_id):
        return self.execute(file_path, game_id, "multipleLanguages", dict(testIndex=3))

    def pk(self, file_path, game_id):
        return self.execute(file_path, game_id, "multi", dict(
            agentsIds=[5604295, -1],
            gameOptions=None,
            isSoloLeague=False
        ))

    def run(self, name):
        c = Module().load_module(f'app.yly.codingame.{name}')
        if c.Solution.game_type == 'pk':
            info = self.pk(c.__file__, c.Solution.gameid)
        else:
            info = self.solve(c.__file__, c.Solution.gameid)
        info.update(c.Solution.get_info(**info))
        File(f"data/log/codingame/{name}.json").write_file(info)


if __name__ == "__main__":
    CodingGame().run(sys.argv[1])
