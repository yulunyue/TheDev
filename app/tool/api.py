from typing import Dict
from common.third_util.http import MainHander
from common.tool.export import FrontTable, DomFile
from common.util.export import (
    File,
    get_function_info,
    Node,
    enum_cls,
    search_cls,
    b64_code,
    Dict,
)


class ApiGlobal:
    API_ROUTE = "/app/api"
    UPLOAD_ROOT = File("data/upload").make_dir_if_not_exist(True)

    def query_all_apis(self, **kw):
        return MainHander.POST_API.to_json()

    def get_api_call_info(self, key: str, **kw):
        return get_function_info(MainHander.POST_API.fun_map[key])

    def post_file(self, files: DomFile, **kw):
        if isinstance(files, dict):
            for file_name, body in files.items():
                self.UPLOAD_ROOT.child(file_name).write_file(body)
        ft = FrontTable().set_header("path", "update_time", "size")
        for f in self.UPLOAD_ROOT.list_tree_file():
            ft.append_row(
                path=f.path, update_time=f.get_m_time_str(), size=f.get_size()
            )
        return ft

    def test(
        self,
        a,
        b: enum_cls("a", "b"),
        c: search_cls("/app/api/query_all_apis"),
        d="1",
        **kw,
    ):
        return Node().set_value(dict(a=a, b=b, c=c, d=d))
