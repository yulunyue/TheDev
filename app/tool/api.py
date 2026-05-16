from typing import Dict
from common.third_util.http import MainHandler
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
    logger,
    C,
)


class ApiGlobal(ApiBase):
    idx = 0

    def query_all_apis(self, **kw):
        return FontSearch().add_childs(
            *[Node(value=k) for k in MainHandler.POST_API.fun_map.keys()]
        )

    def get_api_call_info(self, key: str, **kw):
        return get_function_info(MainHandler.POST_API.fun_map[key]).to_json()

    def test(
        self,
        a,
        b: enum_cls("a", "b"),
        c: search_cls("/app/api/query_all_apis"),
        d="1",
        **kw,
    ):
        ApiGlobal.idx += 3
        for i in range(10):
            logger.info(f"{ApiGlobal.idx}{i}xx", extra=C.TOPIC_WEB_LOG)
        return Node(childs=[dict(key=i) for i in range(ApiGlobal.idx)]).set_value(
            dict(a=a, b=b, c=c, d=d)
        )
