from common.util.export import assert_dict
from app.tool.api import ApiGlobal, MainHandler


class TestApi:
    @classmethod
    def setup_class(self):
        MainHandler.POST_API.load_module("/app/api", ApiGlobal)
        self.api: ApiGlobal = ApiGlobal()

    def test_api(self):
        data = self.api.query_all_apis()
        assert_dict(
            [dict(key=v.get_value()) for v in data.childs],
            [
                dict(key="/app/api/get_api_call_info"),
                dict(key="/app/api/query_all_apis"),
                dict(key="/app/api/test"),
            ],
        )

    def test_api1(self):
        assert_dict(
            self.api.get_api_call_info("/app/api/get_api_call_info"),
            {
                "key": "get_api_call_info",
                "title": "get_api_call_info",
                "childs": [
                    {
                        "default_value": None,
                        "is_pos": True,
                        "title": "key",
                        "key": "key",
                        "type": "str",
                    }
                ],
            },
        )

    def test_api2(self):
        assert_dict(
            self.api.get_api_call_info("/app/api/test"),
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
