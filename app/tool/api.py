from typing import Dict
from common.service.export import Node, MainHander, enum_cls, search_cls
from common.util.export import File


class ApiGlobal:
    API_ROUTE = "/app/api"

    def query_api(self, **kw):
        return Node(**MainHander.POST_API.to_json())

    def test(
        self,
        a,
        b: enum_cls(["a", "b"]),
        c: search_cls("/app/api/query_api"),
        d="1",
        **kw,
    ):
        return Node().set_value(f"{[a,b,c,d]}")
