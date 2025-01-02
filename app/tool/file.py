from typing import Dict
from common.service.http import Node,logger
from common.util.fp import File
class Route:
    def read(self,path):
        value=File(path).read_file()
        # logger.info(f'{path}:{value}')
        return Node().set_value(value).to_json()