from typing import Dict
from common.third_util.http import MainHander
from common.util.export import File, get_function_info, Node, enum_cls, search_cls


class ApiGlobal:
    API_ROUTE = "/app/api"

    def query_all_apis(self, **kw):
        return MainHander.POST_API.to_json()

    def get_api_call_info(self, key: str = "", **kw):
        return get_function_info(MainHander.POST_API.fun_map[key]).to_json()

    def test(
        self,
        a,
        b: enum_cls(["a", "b"]),
        c: search_cls("/app/api/query_all_apis"),
        d="1",
        **kw,
    ):
        return Node().set_value(f"{[a,b,c,d]}").to_json()
