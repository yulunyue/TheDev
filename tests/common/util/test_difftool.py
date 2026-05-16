import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.util.difftool import Diff


class TestDiff(unittest.TestCase):
    """测试 Diff 类"""

    def setUp(self):
        """设置测试环境"""
        self.diff = Diff({"a": 1, "b": 2})
        self.target = {"a": 1, "b": 3, "c": 4}

    def test_diff_creation(self):
        """测试 Diff 创建"""
        self.assertIsInstance(self.diff, Diff)
        self.assertEqual(self.diff.src, {"a": 1, "b": 2})
        self.assertEqual(self.diff.key_join_char, "/")
        self.assertEqual(self.diff.diff_result, [])

    def test_compare_simple_change(self):
        """测试简单变化的比较"""
        result = self.diff.compare(self.target)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # 应该包含更新操作
        update_found = any("update" in op for op in result)
        self.assertTrue(update_found)

    def test_compare_insertion(self):
        """测试插入操作"""
        src = {}
        target = {"new_key": "new_value"}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含插入操作
        insert_found = any("insert" in op for op in result)
        self.assertTrue(insert_found)

    def test_compare_deletion(self):
        """测试删除操作"""
        src = {"key1": "value1", "key2": "value2"}
        target = {"key1": "value1"}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含删除操作
        delete_found = any("delete" in op for op in result)
        self.assertTrue(delete_found)

    def test_compare_identical(self):
        """测试相同数据的比较"""
        result = self.diff.compare({"a": 1, "b": 2})
        self.assertEqual(result, [])

    def test_is_same_true(self):
        """测试 is_same 返回 True"""
        diff = Diff({"a": 1, "b": 2})
        result = diff.is_same({"a": 1, "b": 2})
        self.assertEqual(result, "")

    def test_is_same_false(self):
        """测试 is_same 返回 False"""
        result = self.diff.is_same({"a": 1, "b": 3})
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_is_same_with_string_input(self):
        """测试字符串输入的 is_same"""
        # 字符串形式的字典
        str_dict = '{"a": 1, "b": 2}'
        diff = Diff({"a": 1, "b": 2})
        result = diff.is_same(str_dict)
        self.assertEqual(result, "")

    def test_is_same_with_string_diff(self):
        """测试字符串与字典的差异"""
        str_dict = '{"a": 1, "b": 3}'
        result = self.diff.is_same(str_dict)
        self.assertNotEqual(result, "")

    def test_insert_method(self):
        """测试 insert 方法"""
        self.diff.insert(["key"], "value")
        self.assertIn("insert[key][value]", self.diff.diff_result)

    def test_delete_method(self):
        """测试 delete 方法"""
        self.diff.delete(["key"], "value")
        self.assertIn("delete[key][value]", self.diff.diff_result)

    def test_diff_method(self):
        """测试 diff 方法"""
        self.diff.diff(["key"], 1, 2)
        self.assertIn("update[key][1][2]", self.diff.diff_result)

    def test_diff_with_float_tolerance(self):
        """测试浮点数容差"""
        # 测试在容差范围内的浮点数
        self.diff.diff(["key"], 1.000001, 1.000002)
        # 应该没有差异记录
        diff_found = any("update" in op for op in self.diff.diff_result)
        self.assertFalse(diff_found)

    def test_diff_outside_float_tolerance(self):
        """测试超出浮点数容差"""
        # 测试超出容差范围的浮点数
        self.diff.diff(["key"], 1.1, 1.2)
        # 应该有差异记录
        diff_found = any("update" in op for op in self.diff.diff_result)
        self.assertTrue(diff_found)

    def test_diff_any_with_dict(self):
        """测试字典类型的递归比较"""
        src = {"a": {"b": 1}}
        target = {"a": {"b": 2, "c": 3}}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含嵌套的更新和插入操作
        self.assertGreater(len(result), 0)

    def test_diff_any_with_list(self):
        """测试列表类型的递归比较"""
        src = {"a": [1, 2, 3]}
        target = {"a": [1, 2, 4, 5]}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含列表元素的更新和插入操作
        self.assertGreater(len(result), 0)

    def test_diff_any_with_nested_structure(self):
        """测试嵌套结构的比较"""
        src = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        target = {"users": [{"id": 1, "name": "Alice"}, {"id": 3, "name": "Charlie"}]}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含嵌套的差异
        self.assertGreater(len(result), 0)

    def test_diff_with_none_values(self):
        """测试 None 值的处理"""
        src = {"a": None, "b": 2}
        target = {"a": 1, "b": None}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含 None 值的变化
        self.assertGreater(len(result), 0)

    def test_diff_result_format(self):
        """测试差异结果的格式"""
        src = {"a": 1}
        target = {"a": 2, "b": 3}
        diff = Diff(src)
        result = diff.compare(target)

        # 检查结果格式
        self.assertIsInstance(result, list)

        # 应该包含目标数据作为第一条
        self.assertTrue(any("ret:" in op for op in result))

        # 应该包含期望数据作为第二条
        self.assertTrue(any("exp:" in op for op in result))

    def test_custom_key_join_char(self):
        """测试自定义键连接符"""
        diff = Diff({"a": 1}, key_join_char=".")
        diff.diff(["p", "q"], 1, 2)
        self.assertIn("update[p.q][1][2]", diff.diff_result[0])

    def test_multiple_operations(self):
        """测试多种操作的组合"""
        src = {"a": 1, "b": 2, "c": 3}
        target = {"a": 1, "b": 4, "d": 5}
        diff = Diff(src)
        result = diff.compare(target)

        # 应该包含更新和插入操作
        update_found = any("update" in op for op in result)
        insert_found = any("insert" in op for op in result)
        self.assertTrue(update_found)
        self.assertTrue(insert_found)

    def test_empty_source_and_target(self):
        """测试空源和空目标"""
        diff = Diff({})
        result = diff.compare({})
        self.assertEqual(result, [])

    def test_empty_source_non_empty_target(self):
        """测试空源非空目标"""
        diff = Diff({})
        result = diff.compare({"a": 1})

        # 应该只包含插入操作
        insert_found = any("insert" in op for op in result)
        self.assertTrue(insert_found)

        # 不应该包含更新或删除操作
        update_found = any("update" in op for op in result)
        delete_found = any("delete" in op for op in result)
        self.assertFalse(update_found)
        self.assertFalse(delete_found)

    def test_non_empty_source_empty_target(self):
        """测试非空源空目标"""
        diff = Diff({"a": 1})
        result = diff.compare({})

        # 应该只包含删除操作
        delete_found = any("delete" in op for op in result)
        self.assertTrue(delete_found)

        # 不应该包含更新或插入操作
        update_found = any("update" in op for op in result)
        insert_found = any("insert" in op for op in result)
        self.assertFalse(update_found)
        self.assertFalse(insert_found)


class TestDiffUtilFunctions(unittest.TestCase):
    """测试 Diff 相关的工具函数"""

    def test_diff_with_complex_data_types(self):
        """测试复杂数据类型的比较"""
        src = {
            "string": "hello",
            "number": 42,
            "float": 3.14159,
            "boolean": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }

        target = {
            "string": "world",
            "number": 42,
            "float": 3.14159,
            "boolean": False,
            "none": "not none",
            "list": [1, 2, 4],
            "dict": {"nested": "changed", "new": "added"},
        }

        diff = Diff(src)
        result = diff.compare(target)

        # 应该检测到各种类型的变化
        self.assertGreater(len(result), 0)

        # 检查具体的变化类型
        changes = [op for op in result if "update" in op]
        self.assertGreater(len(changes), 0)


if __name__ == "__main__":
    unittest.main()
