import unittest
import sys
import os
import io
import json
from unittest.mock import patch, MagicMock

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.mock import MockCf, logger, CT


class TestLogger(unittest.TestCase):
    """测试日志模拟器"""

    def test_logger_creation(self):
        """测试日志记录器创建"""
        self.assertIsNotNone(logger)
        self.assertIsNotNone(logger.info)
        self.assertIsNotNone(logger.map)
        self.assertIsNotNone(logger.debug)
        self.assertIsNotNone(logger.log_tree)
        self.assertIsNotNone(logger.log_grid)

    def test_logger_methods(self):
        """测试日志方法调用"""
        # 这些方法应该是空实现，不应该抛出异常
        logger.info("test message")
        logger.map(key="value")
        logger.debug("debug message")
        logger.log_tree([[1, 2], [2, 3]])
        logger.log_grid(3, 3, lambda i, j: i * j)


class TestCT(unittest.TestCase):
    """测试 CT 常量类"""

    def test_ct_constants(self):
        """测试 CT 常量"""
        self.assertEqual(CT.MOD, (10**9) + 7)
        self.assertEqual(CT.MX, (10**5) + 1)
        self.assertEqual(CT.inf, float("inf"))

    def test_ct_functions(self):
        """测试 CT 工具函数"""
        self.assertEqual(CT.min(1, 2), 1)
        self.assertEqual(CT.max(1, 2), 2)
        self.assertEqual(CT.min(-5, 5), -5)
        self.assertEqual(CT.max(-5, 5), 5)


class TestMockCf(unittest.TestCase):
    """测试 MockCf 类"""

    def setUp(self):
        """设置测试环境"""
        self.mock_cf = MockCf()

    def test_mock_cf_creation(self):
        """测试 MockCf 创建"""
        self.assertIsInstance(self.mock_cf, MockCf)
        self.assertEqual(self.mock_cf.get_cases(), {})
        self.assertIsNone(self.mock_cf.src_file)
        self.assertEqual(self.mock_cf.inputs, [])

    def test_mock_cf_with_function(self):
        """测试带函数的 MockCf"""

        def test_func():
            return "test result"

        mock_cf = MockCf(f=test_func)
        self.assertEqual(mock_cf.execute, test_func)

    def test_mock_cf_with_cases(self):
        """测试带测试用例的 MockCf"""
        cases = {
            "test1": {"input": "1", "result": [1]},
            "test2": {"input": "2", "result": [2]},
        }
        mock_cf = MockCf(cases=cases)
        self.assertEqual(mock_cf.cases, cases)

    def test_get_cases(self):
        """测试获取测试用例"""
        cases = {"test": {"result": "value"}}
        mock_cf = MockCf(cases=cases)
        self.assertEqual(mock_cf.get_cases(), cases)

    def test_set_inputs(self):
        """测试设置输入"""
        inputs = "input1\ninput2\ninput3"
        self.mock_cf.set_inputs(inputs)
        self.assertEqual(self.mock_cf.inputs, ["input1", "input2", "input3"])

    def test_set_inputs_chain(self):
        """测试 set_inputs 链式调用"""
        result = self.mock_cf.set_inputs("input1\ninput2")
        self.assertEqual(result, self.mock_cf)

    def test_input_method(self):
        """测试 input 方法"""
        self.mock_cf.set_inputs("first\nsecond")

        # 第一次调用
        self.assertEqual(self.mock_cf.input(), "first")
        # 第二次调用
        self.assertEqual(self.mock_cf.input(), "second")
        # 第三次调用（应该返回输入提示）
        with patch("builtins.input", return_value="manual_input"):
            result = self.mock_cf.input()
            self.assertEqual(result, "manual_input")

    def test_ii_method(self):
        """测试 ii 方法（整数输入）"""
        self.mock_cf.set_inputs("1 2 3\n4 5 6")

        # 第一次调用
        result1 = self.mock_cf.ii()
        self.assertEqual(result1, [1, 2, 3])

        # 第二次调用
        result2 = self.mock_cf.ii()
        self.assertEqual(result2, [4, 5, 6])

    def test_output_method(self):
        """测试 output 方法"""
        # 测试输出方法（这里只是测试调用不抛出异常）
        try:
            self.mock_cf.output("test message")
            # 如果没有文件写入异常，测试通过
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"output method raised {e}")

    def test_exec_method(self):
        """测试 exec 方法（应该抛出 NotImplementedError()）"""
        with self.assertRaises(NotImplementedError()):
            self.mock_cf.exec()

    def test_run_method(self):

        self.mock_cf.run()

    def test_init_method(self):
        """测试 init 方法（应该抛出 NotImplementedError()）"""
        with self.assertRaises(NotImplementedError()):
            self.mock_cf.init()

    def test_log_method(self):
        """测试 log 方法"""
        # 测试 log 方法不抛出异常
        try:
            self.mock_cf.log(key="value")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"log method raised {e}")

    def test_get_agent_method(self):
        """测试 get_agent 方法"""
        agent = self.mock_cf.get_agent()
        self.assertIsNone(agent)

    def test_execute_method(self):
        """测试 execute 方法"""

        def test_func(*args, **kw):
            return "executed"

        mock_cf = MockCf(f=test_func)
        result = mock_cf.execute("test input")
        self.assertEqual(result, "executed")

    def test_execute_with_inputs(self):
        """测试带输入的 execute 方法"""

        def test_func(a):
            return a

        mock_cf = MockCf(f=test_func)
        result = mock_cf.execute("test input")
        self.assertEqual(result, "test input")


class TestMockCg(unittest.TestCase):
    """测试 MockCg 别名"""

    def test_mock_cg_alias(self):
        """测试 MockCg 是 MockCf 的别名"""
        from common.mock import MockCg

        self.assertEqual(MockCg, MockCf)

        # 测试可以使用 MockCg 创建对象
        mock_obj = MockCg()
        self.assertIsInstance(mock_obj, MockCf)


if __name__ == "__main__":
    unittest.main()
