from common.service.export import Api
from common.util.export import File, List, logger
import json


class CGFrames:
    def load(
        self, stdout="", stderr=None, agentId=None, gameInformation=None, **kw
    ) -> "CGFrames":
        self.stdout = stdout[:-1]
        self.gameInformation = gameInformation
        self.agent_id = agentId
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

    def execute(self, file_path, game_id, key=None, data=None, play_type="play"):
        code = open(file_path, "r", encoding="utf-8").read()
        info = dict(code=code, programmingLanguageId="Python3")
        if key:
            info[key] = data
        player_data = [game_id, info]
        if play_type == "submit":
            player_data.append(None)
        ret = self.post(f"/services/TestSession/{play_type}", player_data)
        tmp_path = self.get_local_path(f"{play_type}.json")
        logger.info(tmp_path)
        File(tmp_path).write_file(ret)
        return ret

    def get_timeout(self):
        return 30

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

    def get_cg_frames(self, name="play") -> List[CGFrames]:
        data = File(self.get_local_path(f"{name}.json")).read_file()
        ret = []
        for d in data["frames"]:
            fr = CGFrames().load(**d)
            if fr.agent_id == -1:
                continue
            ret.append(fr)
        return ret

    _log = None

    def log(self, msg):
        if self._log is None:
            self._log = File(self.get_local_path("replay.log")).get_writer()
        self._log.write(f"{msg}\n")
        self._log.flush()
