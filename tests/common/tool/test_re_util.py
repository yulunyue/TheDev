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

    def test_find_all(self):
        text = "helex"
        self.expect(ReUtil("e").findall(text), ["e", "e"])

    def test_search_lines(self):
        text = """
# xx
```key xx
python xx
```
# xx2
```key2 xx2
python xx2
```
"""
        self.expect(
            ReUtil("```(.*?)\n(.*?)\n```").findall(text),
            [("key xx", "python xx"), ("key2 xx2", "python xx2")],
        )
