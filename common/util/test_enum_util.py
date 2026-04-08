import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.util.enum_util import EnumCls, auto, GLOBAL_ADD


class TestEnumCls(unittest.TestCase):
    """测试 EnumCls 类"""
    
    def setUp(self):
        """设置测试环境"""
        # 重置全局计数器
        global GLOBAL_ADD
        GLOBAL_ADD = 0
    
    def test_enum_cls_creation(self):
        """测试 EnumCls 创建"""
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0
            PENDING = 2
        
        self.assertIsInstance(Status(), EnumCls)
        self.assertEqual(Status().type, "")
    
    def test_enum_to_str_mapping(self):
        """测试枚举值到字符串的映射"""
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0
            PENDING = 2
        
        status_enum = Status()
        
        # 测试所有枚举值的映射
        self.assertEqual(status_enum.to_str(1), "ACTIVE")
        self.assertEqual(status_enum.to_str(0), "INACTIVE")
        self.assertEqual(status_enum.to_str(2), "PENDING")
    
    def test_enum_to_str_with_string_values(self):
        """测试字符串枚举值的映射"""
        class Colors(EnumCls):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"
        
        colors_enum = Colors()
        
        self.assertEqual(colors_enum.to_str("red"), "RED")
        self.assertEqual(colors_enum.to_str("green"), "GREEN")
        self.assertEqual(colors_enum.to_str("blue"), "BLUE")
    
    def test_enum_to_str_nonexistent_value(self):
        """测试不存在的值"""
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0
        
        status_enum = Status()
        
        # 测试不存在的值应该抛出异常
        with self.assertRaises(Exception):
            status_enum.to_str(999)
    
    def test_enum_skips_private_attributes(self):
        """测试跳过私有属性"""
        class TestEnum(EnumCls):
            PUBLIC_VALUE = 1
            _PRIVATE_VALUE = 2
            __PRIVATE_VALUE = 3
        
        test_enum = TestEnum()
        
        # 只有公共属性应该被映射
        self.assertEqual(test_enum.to_str(1), "PUBLIC_VALUE")
        with self.assertRaises(Exception):
            test_enum.to_str(2)  # 私有属性不应该被映射
    
    def test_enum_skips_non_int_string_values(self):
        """测试跳过非 int/string 类型的值"""
        class MixedEnum(EnumCls):
            INT_VALUE = 1
            STR_VALUE = "string"
            LIST_VALUE = [1, 2, 3]  # 应该被跳过
            DICT_VALUE = {"key": "value"}  # 应该被跳过
        
        mixed_enum = MixedEnum()
        
        # 只有 int 和 string 值应该被映射
        self.assertEqual(mixed_enum.to_str(1), "INT_VALUE")
        self.assertEqual(mixed_enum.to_str("string"), "STR_VALUE")
        
        # 其他类型的值不应该被映射
        with self.assertRaises(Exception):
            mixed_enum.to_str([1, 2, 3])
    
    def test_enum_with_custom_init(self):
        """测试自定义初始化"""
        class CustomEnum(EnumCls):
            def init(self):
                self.custom_attr = "custom_value"
        
        custom_enum = CustomEnum()
        self.assertEqual(custom_enum.custom_attr, "custom_value")


class TestAutoFunction(unittest.TestCase):
    """测试 auto 函数"""
    
    def setUp(self):
        """设置测试环境"""
        # 重置全局计数器
        global GLOBAL_ADD
        GLOBAL_ADD = 0
    
    def test_auto_default_behavior(self):
        """测试 auto 的默认行为"""
        # 第一次调用
        value1 = auto()
        self.assertEqual(value1, 0)
        self.assertEqual(GLOBAL_ADD, 1)
        
        # 第二次调用
        value2 = auto()
        self.assertEqual(value2, 1)
        self.assertEqual(GLOBAL_ADD, 2)
        
        # 第三次调用
        value3 = auto()
        self.assertEqual(value3, 2)
        self.assertEqual(GLOBAL_ADD, 3)
    
    def test_auto_with_start_value(self):
        """测试指定起始值"""
        # 设置起始值
        start_value = 100
        result = auto(start_value)
        
        # 返回原值
        self.assertEqual(result, 100)
        self.assertEqual(GLOBAL_ADD, 101)
    
    def test_auto_with_none(self):
        """测试参数为 None"""
        # 设置为 None
        result = auto(None)
        
        # 应该保持当前值不变
        self.assertEqual(result, 0)  # 因为 setUp 中重置为 0
        self.assertEqual(GLOBAL_ADD, 1)
    
    def test_auto_sequential_calls(self):
        """测试连续调用"""
        # 获取一系列值
        values = [auto() for _ in range(5)]
        
        # 应该是递增的序列
        expected = [0, 1, 2, 3, 4]
        self.assertEqual(values, expected)
        
        # 全局计数器应该是 5
        self.assertEqual(GLOBAL_ADD, 5)
    
    def test_auto_with_negative_numbers(self):
        """测试负数起始值"""
        # 设置负数起始值
        auto(-10)
        
        # 下一个值应该是 -9
        next_value = auto()
        self.assertEqual(next_value, -9)
        self.assertEqual(GLOBAL_ADD, -8)


class TestGlobalVariable(unittest.TestCase):
    """测试全局变量"""
    
    def test_global_add_variable(self):
        """测试 GLOBAL_ADD 变量"""
        # 保存原始值
        original_value = GLOBAL_ADD
        
        # 修改值
        GLOBAL_ADD = 42
        self.assertEqual(GLOBAL_ADD, 42)
        
        # 恢复值
        GLOBAL_ADD = original_value


class TestEnumIntegration(unittest.TestCase):
    """测试枚举集成功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 重置全局计数器
        global GLOBAL_ADD
        GLOBAL_ADD = 0
    
    def test_enum_with_auto_values(self):
        """测试 auto 生成的枚举值"""
        class AutoEnum(EnumCls):
            FIRST = auto()
            SECOND = auto()
            THIRD = auto()
        
        auto_enum = AutoEnum()
        
        # 验证枚举值
        self.assertEqual(auto_enum.to_str(0), "FIRST")
        self.assertEqual(auto_enum.to_str(1), "SECOND")
        self.assertEqual(auto_enum.to_str(2), "THIRD")
    
    def test_mixed_enum_values(self):
        """测试混合枚举值"""
        class MixedEnum(EnumCls):
            FIXED = 100
            AUTO1 = auto()
            AUTO2 = auto()
            STRING = "custom"
        
        mixed_enum = MixedEnum()
        
        # 验证所有值的映射
        self.assertEqual(mixed_enum.to_str(100), "FIXED")
        self.assertEqual(mixed_enum.to_str(0), "AUTO1")
        self.assertEqual(mixed_enum.to_str(1), "AUTO2")
        self.assertEqual(mixed_enum.to_str("custom"), "STRING")
    
    def test_enum_inheritance(self):
        """测试枚举继承"""
        class BaseEnum(EnumCls):
            BASE_VALUE = 1
        
        class DerivedEnum(BaseEnum):
            DERIVED_VALUE = 2
        
        derived_enum = DerivedEnum()
        
        # 应该继承基类的映射
        self.assertEqual(derived_enum.to_str(1), "BASE_VALUE")
        self.assertEqual(derived_enum.to_str(2), "DERIVED_VALUE")


class TestEnumEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        """设置测试环境"""
        # 重置全局计数器
        global GLOBAL_ADD
        GLOBAL_ADD = 0
    
    def test_empty_enum(self):
        """测试空枚举"""
        class EmptyEnum(EnumCls):
            pass
        
        empty_enum = EmptyEnum()
        self.assertEqual(empty_enum.type, "")
        
        # 应该没有映射的值
        with self.assertRaises(Exception):
            empty_enum.to_str(0)
    
    def test_enum_with_duplicate_values(self):
        """测试重复值的枚举"""
        class DuplicateEnum(EnumCls):
            VALUE1 = 1
            VALUE2 = 1  # 重复值
        
        duplicate_enum = DuplicateEnum()
        
        # 后面的值会覆盖前面的映射
        self.assertEqual(duplicate_enum.to_str(1), "VALUE2")
    
    def test_enum_with_zero_and_negative(self):
        """测试零和负数值"""
        class NumberEnum(EnumCls):
            ZERO = 0
            NEGATIVE = -1
            POSITIVE = 1
        
        number_enum = NumberEnum()
        
        self.assertEqual(number_enum.to_str(0), "ZERO")
        self.assertEqual(number_enum.to_str(-1), "NEGATIVE")
        self.assertEqual(number_enum.to_str(1), "POSITIVE")


if __name__ == '__main__':
    unittest.main()