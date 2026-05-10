import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.constant import Constant, CT, C


class TestConstant(unittest.TestCase):
    """测试常量模块"""

    def test_constant_attributes(self):
        """测试常量类的属性"""
        # 测试应用常量
        self.assertEqual(C.APP_NAME, "TheDev")
        self.assertEqual(C.CODE_500, 500)
        self.assertEqual(C.CODE_200, 200)
        self.assertEqual(C.TYPE, "type")
        self.assertEqual(C.KEY, "key")
        self.assertEqual(C.DATA, "data")
        self.assertEqual(C.VALUE, "value")
        self.assertEqual(C.METHOD_INSERT_UPDATE, "INSERT_UPDATE")
        self.assertEqual(C.THE_DEV_USER, "the_dev_user")
        self.assertEqual(C.USERNAME, "username")
        self.assertEqual(C.PASSWORD, "password")
        self.assertEqual(C.METHOD_LOGIN, "login")

    def test_ct_attributes(self):
        """测试 CT 类的数学常量"""
        self.assertEqual(CT.MOD, (10**9) + 7)
        self.assertEqual(CT.MX, (10**5) + 1)
        self.assertEqual(CT.inf, float("inf"))

    def test_ct_functions(self):
        """测试 CT 类的工具函数"""
        # 测试最小值函数
        self.assertEqual(CT.min(5, 10), 5)
        self.assertEqual(CT.min(-1, 0), -1)
        self.assertEqual(CT.min(3.5, 2.5), 2.5)

        # 测试最大值函数
        self.assertEqual(CT.max(5, 10), 10)
        self.assertEqual(CT.max(-1, 0), 0)
        self.assertEqual(CT.max(3.5, 2.5), 3.5)

    def test_ct_functions_with_none(self):
        """测试 CT 函数处理 None 值"""
        with self.assertRaises(TypeError):
            CT.min(None, 5)
        with self.assertRaises(TypeError):
            CT.max(5, None)

    def test_ct_functions_with_different_types(self):
        """测试 CT 函数处理不同类型"""
        self.assertEqual(CT.min(5, 10.5), 5)
        self.assertEqual(CT.max(5, 10.5), 10.5)

    def test_constant_instance(self):
        """测试常量实例"""
        self.assertIsInstance(C, Constant)
        self.assertEqual(C.APP_NAME, "TheDev")

    def test_ct_instance(self):
        """测试 CT 实例"""
        self.assertIsInstance(CT, CT.__class__)
        self.assertEqual(CT.MOD, (10**9) + 7)


class TestMathUtil(unittest.TestCase):
    """测试数学工具函数"""

    def test_min_function(self):
        """测试最小值函数"""
        # CT.min 只接受两个参数
        self.assertEqual(CT.min(1, 2), 1)
        self.assertEqual(CT.min(-10, 0), -10)
        self.assertEqual(CT.min(3.14, 2.71), 2.71)

    def test_max_function(self):
        """测试最大值函数"""
        # CT.max 只接受两个参数
        self.assertEqual(CT.max(1, 2), 2)
        self.assertEqual(CT.max(-10, 0), 0)
        self.assertEqual(CT.max(3.14, 2.71), 3.14)

    def test_math_constants(self):
        """测试数学常量"""
        self.assertIsInstance(CT.MOD, int)
        self.assertIsInstance(CT.MX, int)
        self.assertIsInstance(CT.inf, float)

        # 验证常量值
        self.assertTrue(CT.MOD > 0)
        self.assertTrue(CT.MX > 0)
        self.assertEqual(CT.inf, float("inf"))


if __name__ == "__main__":
    unittest.main()
