from typing import Dict
from common.service.http import Node, MainHander
from common.util.fp import File


class Route:
    def query_api(self, **kw):
        return Node(**MainHander.POST_API.to_json())

    def execute_api(self, name, data, **kw):
        pass

    def test_add(self, a, b):
        return dict(code=200, value=a + b)
