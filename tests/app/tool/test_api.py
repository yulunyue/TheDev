from common.util.export import TestBase
from app.tool.api import ApiGlobal, MainHander


class TestApi(TestBase):
    def setup_class(self):
        MainHander.POST_API.load_module(ApiGlobal)
        self.api = ApiGlobal()

    def test_query_api(self):
        data = self.api.query_all_apis()
        self.expect(
            data["childs"],
            [
                dict(key="/app/api/get_api_call_info"),
                dict(key="/app/api/query_all_apis"),
                dict(key="/app/api/test"),
            ],
        )
        self.expect(self.api.get_api_call_info("/app/api/get_api_call_info"))
