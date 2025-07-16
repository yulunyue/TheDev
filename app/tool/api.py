from typing import Dict
from common.service.http import Node, MainHander
from common.util.fp import File


class ApiGlobal:
    API_ROUTE = "/app/tool/api"

    def query_api(self, **kw):
        return Node(**MainHander.POST_API.to_json())

    def execute_api(self, name, data, **kw):
        pass

    def test(self, a, b, **kw):
        return Node().set_value(a + b)
