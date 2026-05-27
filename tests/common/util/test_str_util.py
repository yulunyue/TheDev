"""
StrUtil 测试文件

使用 pytest 框架进行测试
运行方式: pytest common/util/str_util_test.py -v
或者: python -m pytest common/util/str_util_test.py -v
"""

import unittest
from common.util.str_util import StrUtil


class TestStrUtil(unittest.TestCase):
    """测试字符串工具类"""

    def setUp(self):
        """初始化测试环境"""
        self.str_util = StrUtil()

    def test_get_mid_str(self):
        assert self.str_util.get_mid_str("abc", "a", "c") == "b"

    def test_str_util_creation(self):
        """测试 StrUtil 创建"""
        str_util = StrUtil()
        self.assertIsNotNone(str_util)

    def test_match_with_ignore_patterns(self):
        """测试带忽略模式的匹配"""
        str_util = StrUtil()
        str_util.set_ignores(["test", "ignore"])

        # 应该被忽略的模式
        result = str_util.match("this is a test")
        self.assertFalse(result, "应该忽略包含 'test' 的字符串")

        # 不应该被忽略的模式
        result = str_util.match("this is valid")
        self.assertTrue(result, "不应该忽略不包含模式的字符串")

    def test_match_with_any_patterns(self):
        """测试带必须模式的匹配"""
        str_util = StrUtil()
        str_util.set_matchs(["required", "must"])

        # 应该匹配的模式
        result = str_util.match("this is required")
        self.assertTrue(result, "应该匹配包含 'required' 的字符串")

        # 不应该匹配的模式
        result = str_util.match("this is optional")
        self.assertFalse(result, "不应该匹配不包含必须模式的字符串")

    def test_match_with_both_patterns(self):
        """测试同时使用忽略和必须模式"""
        str_util = StrUtil()
        str_util.set_ignores(["ignore"])
        str_util.set_matchs(["required"])

        # 应该匹配的情况：包含必须模式，不包含忽略模式
        result = str_util.match("this is required")
        self.assertTrue(result, "应该匹配包含必须模式且不包含忽略模式的字符串")

        # 不应该匹配的情况：包含忽略模式
        result = str_util.match("this is required but ignore")
        self.assertFalse(result, "不应该匹配包含忽略模式的字符串")

        # 不应该匹配的情况：不包含必须模式
        result = str_util.match("this is optional")
        self.assertFalse(result, "不应该匹配不包含必须模式的字符串")

    def test_match_no_patterns(self):
        """测试没有任何模式时的匹配"""
        str_util = StrUtil()

        # 没有模式时应该总是匹配
        result = str_util.match("any string")
        self.assertTrue(result, "没有模式时应该总是匹配")

    def test_set_ignores_chain(self):
        """测试 set_ignores 的链式调用"""
        str_util = StrUtil()
        result = str_util.set_ignores(["test"])
        self.assertEqual(result, str_util, "set_ignores 应该返回 self")

    def test_set_matchs_chain(self):
        """测试 set_matchs 的链式调用"""
        str_util = StrUtil()
        result = str_util.set_matchs(["test"])
        self.assertEqual(result, str_util, "set_matchs 应该返回 self")

    def test_format_pre0_bin(self):
        """测试二进制格式化"""
        test_cases = [
            (5, 4, "0101"),  # 5 in 4-bit binary
            (10, 8, "00001010"),  # 10 in 8-bit binary
            (255, 8, "11111111"),  # 255 in 8-bit binary
            (0, 4, "0000"),  # 0 in 4-bit binary
        ]

        for num, width, expected in test_cases:
            with self.subTest(num=num, width=width):
                result = self.str_util.format_pre0_bin(num, width)
                self.assertEqual(
                    result, expected, f"Failed for {num} with width {width}"
                )

    def test_format_basic(self):
        """测试基本格式化"""
        template = "Hello %{name}, you are %{age} years old"
        result = self.str_util.format(template, name="Alice", age="25")
        expected = "Hello Alice, you are 25 years old"
        self.assertEqual(result, expected, "基本格式化测试失败")

    def test_format_multiple_placeholders(self):
        """测试多个占位符格式化"""
        template = "%{first} %{middle} %{last}"
        result = self.str_util.format(template, first="John", middle="A", last="Doe")
        expected = "John A Doe"
        self.assertEqual(result, expected, "多个占位符格式化测试失败")

    def test_format_no_placeholders(self):
        """测试没有占位符的格式化"""
        template = "This is a plain string"
        result = self.str_util.format(template)
        expected = "This is a plain string"
        self.assertEqual(result, expected, "没有占位符的格式化测试失败")

    def test_format_empty_template(self):
        """测试空模板格式化"""
        template = ""
        result = self.str_util.format(template, name="test")
        expected = ""
        self.assertEqual(result, expected, "空模板格式化测试失败")

    def test_format_consecutive_placeholders(self):
        """测试连续占位符格式化"""
        template = "%{a}%{b}%{c}"
        result = self.str_util.format(template, a="1", b="2", c="3")
        expected = "123"
        self.assertEqual(result, expected, "连续占位符格式化测试失败")


class TestStrUtilAdvanced(unittest.TestCase):
    """测试 StrUtil 的高级功能"""

    def setUp(self):
        """初始化测试环境"""
        self.str_util = StrUtil()

    def test_format_g_tree_simple(self):
        """测试简单图的树形格式化"""
        graph = [(0, 1), (1, 2)]
        result = self.str_util.format_g_tree(graph, lambda x, d: str(x))
        self.assertIsInstance(result, str, "format_g_tree 应该返回字符串")

    def test_format_g_tree_complex(self):
        """测试复杂图的树形格式化"""
        graph = [(0, 1), (0, 2), (1, 3)]
        result = self.str_util.format_g_tree(graph, lambda x, d: str(x))
        self.assertIsInstance(result, str, "format_g_tree 应该返回字符串")

    def test_format_g_tree_empty(self):
        """测试空图的树形格式化"""
        graph = [(0, 1)]
        result = self.str_util.format_g_tree(graph, lambda x, d: str(x))
        self.assertIsInstance(result, str, "format_g_tree 应该返回字符串")

    def test_format_grid_2x2(self):
        """测试 2x2 网格格式化"""

        grid = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}

        result = self.str_util.format_grid(2, 2, grid)
        self.assertIsInstance(result, str, "format_grid 应该返回字符串")
        self.assertIn("0 0", result, "结果应该包含 '0 0'")
        self.assertIn("0 1", result, "结果应该包含 '0 1'")

    def test_format_grid_3x3(self):
        """测试 3x3 网格格式化"""

        grid = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): 2,
            (1, 0): 1,
            (1, 1): 2,
            (1, 2): 3,
            (2, 0): 2,
            (2, 1): 3,
            (2, 2): 4,
        }

        result = self.str_util.format_grid(3, 3, grid)
        self.assertIsInstance(result, str, "format_grid 应该返回字符串")
        self.assertIn("0", result, "结果应该包含 0")
        self.assertIn("1", result, "结果应该包含 1")
        self.assertIn("2", result, "结果应该包含 2")
        self.assertIn("3", result, "结果应该包含 3")
        self.assertIn("4", result, "结果应该包含 4")

    def test_format_grid_1x1(self):
        """测试 1x1 网格格式化"""

        grid = {(0, 0): 42}

        result = self.str_util.format_grid(1, 1, grid)
        self.assertIsInstance(result, str, "format_grid 应该返回字符串")
        self.assertIn("42", result, "结果应该包含 42")

    def test_format_grid_zero_size(self):
        """测试零大小网格格式化"""

        grid = {}

        result = self.str_util.format_grid(0, 0, grid)
        self.assertIsInstance(result, str, "format_grid 应该返回字符串")


if __name__ == "__main__":
    # 可以直接运行 unittest
    unittest.main()

    # 或者使用 pytest 运行
    # pytest.main([__file__])
