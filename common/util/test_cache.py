import unittest
import sys
import os
import tempfile
import shutil

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.util.cache import Cache, get_cache


class TestCache(unittest.TestCase):
    """测试 Cache 类"""

    def setUp(self):
        """设置测试环境"""
        self.test_cache_name = "test_cache"
        # 确保测试目录存在
        self.test_dir = os.path.join(os.path.dirname(__file__), "..", "data", "cache")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """清理测试环境"""
        # 清理测试文件
        cache_file = os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)

        # 清理全局缓存
        from common.util.cache import CACHE

        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]

    def test_cache_creation(self):
        """测试 Cache 创建"""
        cache = Cache(self.test_cache_name)
        self.assertIsInstance(cache, Cache)
        self.assertEqual(
            cache.fp.path, os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        )
        self.assertEqual(cache.store, {})

    def test_cache_with_initial_data(self):
        """测试带初始数据的缓存"""
        initial_data = {"key1": "value1", "key2": "value2"}
        cache = Cache(self.test_cache_name)
        cache.store.update(initial_data)

        self.assertEqual(cache.store["key1"], "value1")
        self.assertEqual(cache.store["key2"], "value2")

    def test_set_method(self):
        """测试 set 方法"""
        cache = Cache(self.test_cache_name)

        # 设置单个键值对
        result = cache.set("key1", "value1")
        self.assertEqual(result, cache)  # 返回 self 支持链式调用
        self.assertEqual(cache.store["key1"], "value1")

        # 设置多个键值对
        cache.set("key2", "value2")
        self.assertEqual(cache.store["key2"], "value2")

    def test_get_method(self):
        """测试 get 方法"""
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")

        # 测试不存在的键
        with self.assertRaises(KeyError):
            cache.get("nonexistent_key")

    def test_exists_method(self):
        """测试 exists 方法"""
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        self.assertTrue(cache.exists("key1"))
        self.assertTrue(cache.exists("key2"))
        self.assertFalse(cache.exists("nonexistent_key"))

    def test_save_method(self):
        """测试 save 方法"""
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        # 保存到文件
        result = cache.save()
        self.assertEqual(result, cache)  # 返回 self 支持链式调用

        # 验证文件是否创建

        self.assertTrue(cache.fp.exists())

        # 验证文件内容
        import json

        with open(cache.fp.path, "r") as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, {"key1": "value1", "key2": "value2"})

    def test_load_from_file(self):
        """测试从文件加载数据"""
        cache_file = os.path.join(self.test_dir, f"{self.test_cache_name}.json")

        # 创建测试文件
        import json

        test_data = {"key1": "value1", "key2": "value2"}
        with open(cache_file, "w") as f:
            json.dump(test_data, f)

        # 创建缓存实例（应该自动加载）
        cache = Cache(self.test_cache_name)
        self.assertEqual(cache.store, test_data)

    def test_cache_with_complex_data(self):
        """测试复杂数据类型的缓存"""
        cache = Cache(self.test_cache_name)
        complex_data = {
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
        }

        cache.store = complex_data
        self.assertEqual(cache.store, complex_data)

        # 保存和加载
        cache.save()
        cache2 = Cache(self.test_cache_name)
        self.assertEqual(cache2.store, complex_data)


class TestGetCache(unittest.TestCase):
    """测试 get_cache 函数"""

    def setUp(self):
        """设置测试环境"""
        self.test_cache_name = "test_global_cache"
        # 确保测试目录存在
        self.test_dir = os.path.join(os.path.dirname(__file__), "..", "data", "cache")
        os.makedirs(self.test_dir, exist_ok=True)

        # 清理全局缓存
        from common.util.cache import CACHE

        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]

    def tearDown(self):
        """清理测试环境"""
        # 清理全局缓存
        from common.util.cache import CACHE

        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]

        # 清理测试文件
        cache_file = os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)

    def test_get_cache_first_time(self):
        """测试第一次获取缓存"""
        cache = get_cache(self.test_cache_name)
        self.assertIsInstance(cache, Cache)
        self.assertEqual(
            cache.fp.path, os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        )

        # 验证全局缓存
        from common.util.cache import CACHE

        self.assertIn(self.test_cache_name, CACHE)
        self.assertEqual(CACHE[self.test_cache_name], cache)

    def test_get_cache_second_time(self):
        """测试第二次获取缓存（应该返回相同的实例）"""
        cache1 = get_cache(self.test_cache_name)
        cache2 = get_cache(self.test_cache_name)

        self.assertIs(cache1, cache2)  # 应该是同一个实例

    def test_get_cache_with_data(self):
        """测试获取带数据的缓存"""
        # 先创建一个带数据的缓存
        cache1 = get_cache(self.test_cache_name)
        cache1.set("key1", "value1")
        cache1.save()

        # 获取缓存并验证数据
        cache2 = get_cache(self.test_cache_name)
        self.assertEqual(cache2.get("key1"), "value1")

    def test_multiple_caches(self):
        """测试多个不同的缓存实例"""
        cache1 = get_cache("cache1")
        cache2 = get_cache("cache2")

        # 设置不同的数据
        cache1.set("key", "value1")
        cache2.set("key", "value2")

        # 验证数据不同
        self.assertEqual(cache1.get("key"), "value1")
        self.assertEqual(cache2.get("key"), "value2")

        # 验证是不同的实例
        self.assertIsNot(cache1, cache2)

        # 验证全局缓存中有两个实例
        from common.util.cache import CACHE

        self.assertIn("cache1", CACHE)
        self.assertIn("cache2", CACHE)
        self.assertEqual(len(CACHE), 2)


class TestCacheIntegration(unittest.TestCase):
    """测试缓存集成功能"""

    def setUp(self):
        """设置测试环境"""
        self.test_cache_name = "integration_test"
        self.test_dir = os.path.join(os.path.dirname(__file__), "..", "data", "cache")
        os.makedirs(self.test_dir, exist_ok=True)

        # 清理全局缓存
        from common.util.cache import CACHE

        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]

    def tearDown(self):
        """清理测试环境"""
        # 清理全局缓存
        from common.util.cache import CACHE

        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]

        # 清理测试文件
        cache_file = os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)

    def test_cache_workflow(self):
        """测试完整的工作流程"""
        # 获取缓存实例
        cache = get_cache(self.test_cache_name)

        # 设置数据
        cache.set("name", "Test User")
        cache.set("score", 100)
        cache.set("active", True)

        # 验证数据
        self.assertEqual(cache.get("name"), "Test User")
        self.assertEqual(cache.get("score"), 100)
        self.assertEqual(cache.get("active"), True)
        self.assertTrue(cache.exists("name"))
        self.assertFalse(cache.exists("nonexistent"))

        # 保存到文件
        cache.save()

        # 验证文件存在
        cache_file = os.path.join(self.test_dir, f"{self.test_cache_name}.json")
        self.assertTrue(os.path.exists(cache_file))

        # 创建新实例并验证数据持久化
        cache2 = get_cache(self.test_cache_name)
        self.assertEqual(cache2.get("name"), "Test User")
        self.assertEqual(cache2.get("score"), 100)
        self.assertEqual(cache2.get("active"), True)


if __name__ == "__main__":
    unittest.main()
