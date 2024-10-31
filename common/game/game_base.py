from typing import List
from common.util.fp import File
from common.util.log import logger
from common.util.yml import yml_to_dict


class Base:
    def __init__(self, name) -> None:
        self.name = name


class Node:
    def __init__(self, *childs, value=None) -> None:
        self.value = value
        self.childs = list(childs)

    def to_str(self):
        return f'{self.value}'

    def init(self):
        return self

    def load_from_yml(self, yml):
        logger.info(yml_to_dict(yml))


class PlayerBase(Base):

    def pre_run(self):
        logger.info(f'{self.name}->pre_run')

    def execute(self, env: Node):
        pass

    def run(self, *args, **kg):
        return self.execute(*args, **kg)


class GameBase:
    name = "test"

    def set_player(self, player):
        self.player: List[PlayerBase] = player
        return self

    def do_action(self, action):
        pass

    def run_before(self):
        pass

    def get_game_round(self):
        return 0

    def init(self):
        pass

    def run(self):
        self.init()
        for i in range(self.get_game_round()):
            logger.info(f"begin:---{i}---")
            action = self.player[i % len(self.player)].run(i, self.env)
            self.do_action(action)
            self.run_after()
            logger.info(f"finish:---{i}---")

    def run_after(self):
        pass

    def get_env(self, current_round):
        pass
