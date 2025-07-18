from common.util.export import logger
from app.yly.game.envs.oa.shape.rooms import Rooms
from common.mock import MockBase
class CgOa(MockBase):
    uri='https://www.codingame.com/ide/puzzle/oware-abapa'
    def main(self):
        r=Rooms()
        while True:
            r.set_rooms(self.il())
            self.output(self.r.execute())