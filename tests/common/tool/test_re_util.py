from common.util.test import TestBase
from common.tool.export import ReUtil


class TestReUtil(TestBase):
    def test_search(self):
        text = "Hello, my phone number is 123-456-7890"
        self.expect(ReUtil(r"\d{3}-\d{3}-\d{4}").search(text), "123-456-7890")

    def test_match(self):
        text = "helex"
        self.expect(ReUtil("he").match(text), "he")
        self.expect(ReUtil(".*e").match(text), "hele")
        self.expect(ReUtil(r".*?e").match(text), "he")
