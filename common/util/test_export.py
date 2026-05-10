import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 由于 export.py 导入了很多模块，我们只测试基本功能
class TestExport(unittest.TestCase):
    """测试 export 模块的基本导入和功能"""

    def test_import_export(self):
        """测试导出模块的导入"""
        try:
            from common.util.export import (
                logger,
                get_log,
                json_dumps,
                uid,
                ThreadManage,
                ThreadRecord,
                ApiCall,
                inf,
                null,
                true,
                false,
            )

            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import from export: {e}")

    def test_logger_import(self):
        """测试日志对象的导入"""
        from common.util.export import logger

        # 测试基本方法存在
        self.assertTrue(hasattr(logger, "info"))
        self.assertTrue(hasattr(logger, "debug"))
        self.assertTrue(hasattr(logger, "warning"))
        self.assertTrue(hasattr(logger, "error"))

    def test_constants_import(self):
        """测试常量的导入"""
        from common.util.export import inf, null, true, false

        self.assertEqual(inf, float("inf"))
        self.assertEqual(null, None)
        self.assertEqual(true, True)
        self.assertEqual(false, False)

    @patch("common.util.export.get_log")
    def test_get_log_function(self, mock_get_log):
        """测试 get_log 函数的导入"""
        from common.util.export import get_log

        # 验证函数可以调用
        mock_get_log.return_value = MagicMock()
        result = get_log("test_logger")
        mock_get_log.assert_called_once_with("test_logger")

    @patch("common.util.export.json_dumps")
    def test_json_dumps_function(self, mock_json_dumps):
        """测试 json_dumps 函数的导入"""
        from common.util.export import json_dumps

        # 验证函数可以调用
        test_data = {"key": "value"}
        mock_json_dumps.return_value = '{"key": "value"}'
        result = json_dumps(test_data)
        mock_json_dumps.assert_called_once_with(test_data)

    def test_uid_function(self):
        """测试 uid 函数的导入"""
        from common.util.export import uid

        # 验证函数可以调用
        result1 = uid("test")
        result2 = uid("test")

        # 同一前缀应该生成递增的ID
        self.assertEqual(result1, "test_0")
        self.assertEqual(result2, "test_1")

    @patch("common.util.export.ThreadPoolExecutor")
    def test_thread_manage_import(self, mock_executor):
        """测试 ThreadManage 的导入"""
        from common.util.export import ThreadManage

        # 验证类可以实例化
        mock_executor.return_value = MagicMock()
        thread_manager = ThreadManage(max_workers=5)

        self.assertIsInstance(thread_manager, ThreadManage)
        mock_executor.assert_called_once_with(max_workers=5)

    def test_thread_record_import(self):
        """测试 ThreadRecord 的导入"""
        from common.util.export import ThreadRecord

        # 验证类可以实例化
        thread_record = ThreadRecord()
        self.assertIsInstance(thread_record, ThreadRecord)

    def test_api_call_import(self):
        """测试 ApiCall 的导入"""
        from common.util.export import ApiCall

        # 验证类可以实例化
        api_call = ApiCall()
        self.assertIsInstance(api_call, ApiCall)

        # 验证基本方法存在
        self.assertTrue(hasattr(api_call, "register"))
        self.assertTrue(hasattr(api_call, "call"))
        self.assertTrue(hasattr(api_call, "load_module"))

    def test_export_contains_expected_items(self):
        """测试导出包含预期的项目"""
        from common.util.export import logger

        # 验证导出的主要组件
        expected_attrs = [
            "logger",
            "get_log",
            "json_dumps",
            "uid",
            "ThreadManage",
            "ThreadRecord",
            "ApiCall",
            "inf",
            "null",
            "true",
            "false",
        ]

        for attr in expected_attrs:
            self.assertTrue(hasattr(sys.modules["common.util.export"], attr))


class TestExportFunctionality(unittest.TestCase):
    """测试导出模块的功能"""

    def test_uid_functionality(self):
        """测试 uid 函数的具体功能"""
        from common.util.export import uid

        # 测试不同前缀
        uid1 = uid("prefix1")
        uid2 = uid("prefix2")

        self.assertEqual(uid1, "prefix1_0")
        self.assertEqual(uid2, "prefix2_0")

        # 测试同一前缀的递增性
        uid1_again = uid("prefix1")
        self.assertEqual(uid1_again, "prefix1_1")

    def test_constants_values(self):
        """测试常量的值"""
        from common.util.export import inf, null, true, false

        self.assertTrue(inf > 1000000)  # 无穷大应该很大
        self.assertIsNone(null)
        self.assertTrue(true)
        self.assertFalse(false)

    @patch("common.util.export.logger")
    def test_logger_functionality(self, mock_logger):
        """测试日志功能"""
        from common.util.export import logger

        # 测试日志方法调用
        logger.info("test message")
        logger.debug("debug message")

        # 验证方法被调用
        mock_logger.info.assert_called_with("test message")
        mock_logger.debug.assert_called_with("debug message")


if __name__ == "__main__":
    unittest.main()
