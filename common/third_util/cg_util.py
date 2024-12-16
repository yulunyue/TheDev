from common.service.api import Api, StrModel
import sys
from common.util.module import Module
from common.util.log import logger
from common.util.fp import File
import json


class CodingGame(Api):
    def __init__(self,name):
        self.name = name
        self.log_json = File(f"data/log/cg/{self.name}.json")
    


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

    def pk(self, file_path, game_id, agentsIds):
        ret = self.execute(file_path, game_id, "multi", dict(
            agentsIds=agentsIds,
            gameOptions=None,
            isSoloLeague=False
        ))
        self.log_json.write_file(ret)
    
    def get_states(self):
        states = self.log_json.read_file()
        lines = []
        for frame in states['frames']:
            if 'stderr' in frame:
                lines.extend(frame['stderr'].split('\n'))
        return lines



if __name__ == "__main__":
    CodingGame().run(sys.argv[1])
