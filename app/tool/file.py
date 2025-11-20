from typing import Dict
from common.service.http import Node
from common.util.export import File

LOCAL_ROOT_DIR = "data/temp"


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

    def get(self):
        pass

    def list(self, path="", **kw):
        ret = []
        for f in File(LOCAL_ROOT_DIR).list_dir():
            ret.append(f"<a>{f.name}</a>")
        return "\n".join(ret)
