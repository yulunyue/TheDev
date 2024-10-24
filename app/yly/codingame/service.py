from common.service.api import Api, StrModel
import sys
from common.util.module import Module
from common.util.log import logger


class CodingGame(Api):

    def execute(self, file_path, game_id):
        code = open(file_path, 'r').read()
        player_data = [game_id, {
            "code": code,
            "programmingLanguageId": "Python3",
            "multipleLanguages": {
                "testIndex": 3
            }
        }]
        ret = self.post(
            '/services/TestSession/play', player_data)
        return ret

    def run(self, name):
        c = Module().load_module(f'app.yly.codingame.{name}')
        info = self.execute(c.__file__, c.Solution.gameid)
        logger.info(info)


if __name__ == "__main__":
    CodingGame().run(sys.argv[1])
