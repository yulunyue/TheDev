from common.util.export import logger
from app.yly.game.envs.oa.model.state import Rooms
from common.mock import MockCf


class CgOa(MockCf):
    uri = "https://www.codingame.com/ide/puzzle/oware-abapa"

    def main(self):
        r = Rooms()
        while True:
            r.set_rooms(self.il())
            self.output(self.r.execute())


if __name__ == "__main__":
    CgOa().main()
