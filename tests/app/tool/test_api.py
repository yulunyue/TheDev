from common.util.export import TestBase
from app.tool.api import ApiGlobal, MainHander


class TestApi(TestBase):
    api: ApiGlobal

    @classmethod
    def setup_class(cls):
        MainHander.POST_API.load_module(ApiGlobal)
        cls.api: ApiGlobal = ApiGlobal()

    def test_api(self):
        data = self.api.query_all_apis()
        self.expect(
            data["childs"],
            [
                dict(key="/app/api/get_api_call_info"),
                dict(key="/app/api/query_all_apis"),
                dict(key="/app/api/test"),
            ],
        )

    def test_api1(self):
        self.expect(
            TestApi.api.get_api_call_info("/app/api/get_api_call_info"),
            {
                "key": "get_api_call_info",
                "childs": [
                    {
                        "default_value": None,
                        "is_pos": True,
                        "title": "key",
                        "key": "key",
                        "type": "str",
                    }
                ],
                "title": "get_api_call_info",
            },
        )

    def test_api2(self):
        e = TestApi.api.get_api_call_info("/app/api/test")
        self.expect(
            e,
            {
                "key": "test",
                "title": "test",
                "childs": [
                    {
                        "title": "a",
                        "default_value": "1",
                        "type": "str",
                        "is_pos": False,
                        "key": "a",
                    },
                    {
                        "title": "b",
                        "default_value": None,
                        "type": "enum",
                        "is_pos": False,
                        "childs": ["a", "b"],
                        "key": "b",
                    },
                    {
                        "title": "c",
                        "default_value": None,
                        "type": "search",
                        "is_pos": False,
                        "url": "/app/api/query_all_apis",
                        "key": "c",
                    },
                    {
                        "title": "d",
                        "default_value": None,
                        "type": None,
                        "is_pos": False,
                        "key": "d",
                    },
                ],
            },
        )
