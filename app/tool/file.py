from typing import Dict
from common.service.http import Node
from common.util.fp import File
class Route:
    def read(self, path):
        value=File(path).read_file()
        return Node().set_value(value).to_json()