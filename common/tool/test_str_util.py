from common.util.export import TestBase
from common.tool.export import StrUtil


class TestStrUtil(TestBase):
    def test_format_g_tree(self):
        self.expect(
            StrUtil().format_g_tree(
                [[0, 1], [0, 2]],
                lambda v, depth: f"a{v}",
            ),
            """---
-0: a0
  -1: a1
  -2: a2
---""",
        )
