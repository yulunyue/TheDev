from typing import Dict
from common.service.http import Node
from common.util.fp import File


class FileManage:
    API_ROUTE = "/app/file"

    def read(self, path="", **kw):
        value = File(path).read_file()
        if isinstance(value, dict):
            return Node().set_data(**value)
        return Node().set_value(value)

    def write(self, path="", **kw):
        File(path).write_file(kw)
        return Node()
