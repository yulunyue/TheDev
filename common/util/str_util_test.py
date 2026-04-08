import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestStrUtil(unittest.TestCase):
    """测试字符串工具类"""
    
    def setUp(self):
        """设置测试环境"""
        from common.tool.str_util import StrUtil
        self.str_util = StrUtil()
    
    def test_str_util_creation(self):
        """测试 StrUtil 创建"""
        from common.tool.str_util import StrUtil
        str_util = StrUtil()
        self.assertIsNotNone(str_util)
    
    def test_format_g_tree(self):
        """测试格式化树形结构"""
        from common.tool.str_util import StrUtil
        
        # 简单的树形结构
        tree = [[1, 2], [2, 3], [3, 4]]
        result = StrUtil().format_g_tree(tree)
        
        self.assertIsInstance(result, str)
        self.assertIn("1", result)
        self.assertIn("2", result)
        self.assertIn("3", result)
    
    def test_format_grid(self):
        """测试格式化网格"""
        from common.tool.str_util import StrUtil
        
        def grid_func(i, j):
            return i * j
        
        result = StrUtil().format_grid(3, 3, grid_func)
        
        self.assertIsInstance(result, str)
        # 应该包含数字和换行符
        self.assertIn("0", result)
        self.assertIn("1", result)
        self.assertIn("2", result)
    
    def test_to_camel_case(self):
        """测试转换为驼峰命名"""
        from common.tool.str_util import StrUtil
        
        # 测试各种转换情况
        test_cases = [
            ("hello_world", "helloWorld"),
            ("HELLO_WORLD", "helloWorld"),
            ("hello", "hello"),
            ("h", "h"),
            ("", ""),
            ("a_b_c_d", "aBCD")
        ]
        
        for snake_case, expected in test_cases:
            with self.subTest(snake_case=snake_case):
                result = StrUtil().to_camel_case(snake_case)
                self.assertEqual(result, expected)
    
    def test_to_snake_case(self):
        """测试转换为蛇形命名"""
        from common.tool.str_util import StrUtil
        
        # 测试各种转换情况
        test_cases = [
            ("helloWorld", "hello_world"),
            ("HelloWorld", "hello_world"),
            ("hello", "hello"),
            ("h", "h"),
            ("", ""),
            ("aBCD", "a_b_c_d"),
            ("XMLParser", "xml_parser")
        ]
        
        for camel_case, expected in test_cases:
            with self.subTest(camel_case=camel_case):
                result = StrUtil().to_snake_case(camel_case)
                self.assertEqual(result, expected)
    
    def test_escape_html(self):
        """测试 HTML 转义"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("<div>", "&lt;div&gt;"),
            ("&", "&amp;"),
            ('"', "&quot;"),
            ("'", "&#39;"),
            ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;"),
            ("normal text", "normal text")
        ]
        
        for html_text, expected in test_cases:
            with self.subTest(html_text=html_text):
                result = StrUtil().escape_html(html_text)
                self.assertEqual(result, expected)
    
    def test_unescape_html(self):
        """测试 HTML 反转义"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("&lt;div&gt;", "<div>"),
            ("&amp;", "&"),
            ('&quot;', '"'),
            ("&#39;", "'"),
            ("&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;", "<script>alert('xss')</script>"),
            ("normal text", "normal text")
        ]
        
        for escaped_text, expected in test_cases:
            with self.subTest(escaped_text=escaped_text):
                result = StrUtil().unescape_html(escaped_text)
                self.assertEqual(result, expected)
    
    def test_truncate(self):
        """测试字符串截断"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("hello world", 5, "...", "hello..."),
            ("hello world", 11, "...", "hello world"),
            ("hello world", 0, "...", "..."),
            ("hello world", 5, "", "hello"),
            ("", 5, "...", ""),
        ]
        
        for text, length, suffix, expected in test_cases:
            with self.subTest(text=text, length=length):
                result = StrUtil().truncate(text, length, suffix)
                self.assertEqual(result, expected)
    
    def test_pad_left(self):
        """测试左填充"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("1", 3, "0", "001"),
            ("hello", 5, " ", "hello"),
            ("hello", 10, " ", "     hello"),
            ("hello", 3, "0", "hello"),  # 不截断
            ("", 3, "0", "000")
        ]
        
        for text, width, char, expected in test_cases:
            with self.subTest(text=text, width=width):
                result = StrUtil().pad_left(text, width, char)
                self.assertEqual(result, expected)
    
    def test_pad_right(self):
        """测试右填充"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("1", 3, "0", "100"),
            ("hello", 5, " ", "hello"),
            ("hello", 10, " ", "hello     "),
            ("hello", 3, "0", "hello"),  # 不截断
            ("", 3, "0", "000")
        ]
        
        for text, width, char, expected in test_cases:
            with self.subTest(text=text, width=width):
                result = StrUtil().pad_right(text, width, char)
                self.assertEqual(result, expected)
    
    def test_reverse(self):
        """测试字符串反转"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("hello", "olleh"),
            ("", ""),
            ("a", "a"),
            ("12345", "54321"),
            ("racecar", "racecar")  # 回文
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = StrUtil().reverse(text)
                self.assertEqual(result, expected)
    
    def test_is_palindrome(self):
        """测试回文判断"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("racecar", True),
            ("hello", False),
            ("", True),
            ("a", True),
            ("A man a plan a canal Panama", True),  # 忽略大小写和空格
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = StrUtil().is_palindrome(text)
                self.assertEqual(result, expected)
    
    def test_count_chars(self):
        """测试字符统计"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
            ("aaa", {"a": 3}),
            ("", {}),
            ("a b c", {"a": 1, " ": 2, "b": 1, "c": 1})
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = StrUtil().count_chars(text)
                self.assertEqual(result, expected)
    
    def test_remove_duplicates(self):
        """测试去重"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("hello", "helo"),
            ("aabbcc", "abc"),
            ("", ""),
            ("a", "a"),
            ("112233", "123")
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = StrUtil().remove_duplicates(text)
                self.assertEqual(result, expected)
    
    def test_to_words(self):
        """测试分词"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            ("hello world", ["hello", "world"]),
            ("  hello   world  ", ["hello", "world"]),  # 处理多余空格
            ("", []),
            ("single", ["single"]),
            ("word1 word2", ["word1", "word2"])
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = StrUtil().to_words(text)
                self.assertEqual(result, expected)
    
    def test_join_words(self):
        """测试连接单词"""
        from common.tool.str_util import StrUtil
        
        test_cases = [
            (["hello", "world"], " ", "hello world"),
            ([], " ", ""),
            (["single"], "-", "single"),
            (["a", "b", "c"], ",", "a,b,c")
        ]
        
        for words, separator, expected in test_cases:
            with self.subTest(words=words):
                result = StrUtil().join_words(words, separator)
                self.assertEqual(result, expected)


class TestStrUtilEdgeCases(unittest.TestCase):
    """测试 StrUtil 的边界情况"""
    
    def test_with_none_input(self):
        """测试 None 输入"""
        from common.tool.str_util import StrUtil
        
        str_util = StrUtil()
        
        with self.assertRaises(AttributeError):
            str_util.to_camel_case(None)
        
        with self.assertRaises(AttributeError):
            str_util.truncate(None, 5)
    
    def test_with_non_string_input(self):
        """测试非字符串输入"""
        from common.tool.str_util import StrUtil
        
        str_util = StrUtil()
        
        with self.assertRaises(AttributeError):
            str_util.to_camel_case(123)
        
        with self.assertRaises(AttributeError):
            str_util.escape_html(123.5)


if __name__ == '__main__':
    unittest.main()