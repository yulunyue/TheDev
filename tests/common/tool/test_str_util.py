from common.util.export import TestBase, StrUtil


class TestStrUtil(TestBase):
    def test_format_g_tree(self):
        self.expect(
            StrUtil().format_g_tree(
                [[1, 2]],
                lambda v: f"a{v}",
            ),
            """---
-0: a0
  -1: a1
  -2: a2
---""",
        )
