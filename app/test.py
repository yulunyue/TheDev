from common.export import TestBase
from app.tool.export import ApiRoute


class TestTheDev(TestBase):
    def test_api(self):
        api = ApiRoute()
        self.expect(api.query_api().to_json(), [])
