from common.util.export import TestBase
from app.tool.api import ApiGlobal, MainHander


class TestApi(TestBase):
    def setup_class(self):
        MainHander.POST_API.load_module(ApiGlobal)
        self.api = ApiGlobal()

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
        self.expect(
            self.api.get_api_call_info("/app/api/get_api_call_info"),
            {
                "key": "get_api_call_info",
                "data": {
                    "key": {
                        "default_value": None,
                        "is_pos": True,
                        "title": "key",
                        "type": "str",
                    }
                },
                "title": "get_api_call_info",
            },
        )

    def test_api2(self):
        e = self.api.get_api_call_info("/app/api/test")
        self.expect(
            e,
            {
                "key": "test",
                "title": "test",
                "data": {
                    "a": {
                        "title": "a",
                        "default_value": None,
                        "type": None,
                        "is_pos": True,
                    },
                    "b": {
                        "title": "b",
                        "default_value": "1",
                        "type": "enum",
                        "is_pos": False,
                        "childs": ["a", "b"],
                    },
                    "c": {
                        "title": "c",
                        "default_value": None,
                        "type": "search",
                        "is_pos": False,
                        "url": "/app/api/query_api",
                    },
                    "d": {
                        "title": "d",
                        "default_value": None,
                        "type": None,
                        "is_pos": False,
                    },
                },
            },
        )
