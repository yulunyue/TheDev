from typing import Dict
from common.third_util.http import MainHander
from common.tool.export import FrontTable, DomFile, FontSearch
from common.util.export import (
    File,
    get_function_info,
    Node,
    enum_cls,
    search_cls,
    b64_code,
    Dict,
    ApiBase,
)


class ApiGlobal(ApiBase):

    def query_all_apis(self, **kw):
        return FontSearch().add_node(*MainHander.POST_API.fun_map.keys())

    def get_api_call_info(self, key: str, **kw):
        return get_function_info(MainHander.POST_API.fun_map[key])

    def test(
        self,
        a,
        b: enum_cls("a", "b"),
        c: search_cls("/app/api/query_all_apis"),
        d="1",
        **kw,
    ):
        return Node().set_value(dict(a=a, b=b, c=c, d=d))
