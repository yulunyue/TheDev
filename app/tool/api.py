from typing import Dict
from common.service.http import Node, MainHander
from common.util.fp import File


class ApiGlobal:
    def query_api(self, **kw):
        return Node(**MainHander.POST_API.to_json())

    def execute_api(self, name, data, **kw):
        pass
