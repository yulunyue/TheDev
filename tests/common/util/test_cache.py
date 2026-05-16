import unittest
import json
import os
import shutil

from common.util.cache import Cache, get_cache, CACHE


class TestCache(unittest.TestCase):

    def setUp(self):
        self.test_cache_name = "test_cache"
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]
        cache_path = f"data/cache/{self.test_cache_name}.json"
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def test_cache_creation(self):
        cache = Cache(self.test_cache_name)
        self.assertIsInstance(cache, Cache)
        self.assertEqual(cache.fp.path, f"data/cache/{self.test_cache_name}.json")
        self.assertEqual(cache.store, {})

    def test_cache_with_initial_data(self):
        initial_data = {"key1": "value1", "key2": "value2"}
        cache = Cache(self.test_cache_name)
        cache.store.update(initial_data)

        self.assertEqual(cache.store["key1"], "value1")
        self.assertEqual(cache.store["key2"], "value2")

    def test_set_method(self):
        cache = Cache(self.test_cache_name)

        result = cache.set("key1", "value1")
        self.assertEqual(result, cache)
        self.assertEqual(cache.store["key1"], "value1")

        cache.set("key2", "value2")
        self.assertEqual(cache.store["key2"], "value2")

    def test_get_method(self):
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")

        with self.assertRaises(KeyError):
            cache.get("nonexistent_key")

    def test_exists_method(self):
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        self.assertTrue(cache.exists("key1"))
        self.assertTrue(cache.exists("key2"))
        self.assertFalse(cache.exists("nonexistent_key"))

    def test_save_method(self):
        cache = Cache(self.test_cache_name)
        cache.store = {"key1": "value1", "key2": "value2"}

        result = cache.save()
        self.assertEqual(result, cache)
        self.assertTrue(cache.fp.exists())

        import json

        with open(cache.fp.path, "r") as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, {"key1": "value1", "key2": "value2"})

    def test_load_from_file(self):
        cache_path = f"data/cache/{self.test_cache_name}.json"
        os.makedirs("data/cache", exist_ok=True)

        test_data = {"key1": "value1", "key2": "value2"}
        with open(cache_path, "w") as f:
            json.dump(test_data, f)

        cache = Cache(self.test_cache_name)
        self.assertEqual(cache.store, test_data)

    def test_cache_with_complex_data(self):
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

        cache.save()
        cache2 = Cache(self.test_cache_name)
        self.assertEqual(cache2.store, complex_data)


class TestGetCache(unittest.TestCase):

    def setUp(self):
        self.test_cache_name = "test_global_cache"
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]
        cache_path = f"data/cache/{self.test_cache_name}.json"
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def test_get_cache_first_time(self):
        cache = get_cache(self.test_cache_name)
        self.assertIsInstance(cache, Cache)
        self.assertEqual(cache.fp.path, f"data/cache/{self.test_cache_name}.json")

        self.assertIn(self.test_cache_name, CACHE)
        self.assertEqual(CACHE[self.test_cache_name], cache)

    def test_get_cache_second_time(self):
        cache1 = get_cache(self.test_cache_name)
        cache2 = get_cache(self.test_cache_name)

        self.assertIs(cache1, cache2)

    def test_get_cache_with_data(self):
        cache1 = get_cache(self.test_cache_name)
        cache1.set("key1", "value1")
        cache1.save()

        cache2 = get_cache(self.test_cache_name)
        self.assertEqual(cache2.get("key1"), "value1")

    def test_multiple_caches(self):
        cache1 = get_cache("cache1")
        cache2 = get_cache("cache2")

        cache1.set("key", "value1")
        cache2.set("key", "value2")

        self.assertEqual(cache1.get("key"), "value1")
        self.assertEqual(cache2.get("key"), "value2")

        self.assertIsNot(cache1, cache2)

        self.assertIn("cache1", CACHE)
        self.assertIn("cache2", CACHE)
        self.assertEqual(len(CACHE), 2)

    def test_get_cache_without_cleanup_between_calls(self):
        cache = get_cache(self.test_cache_name)
        cache.set("name", "Test User")
        cache.set("score", 100)
        cache.set("active", True)

        self.assertEqual(cache.get("name"), "Test User")
        self.assertEqual(cache.get("score"), 100)
        self.assertEqual(cache.get("active"), True)
        self.assertTrue(cache.exists("name"))
        self.assertFalse(cache.exists("nonexistent"))


class TestCacheIntegration(unittest.TestCase):

    def setUp(self):
        self.test_cache_name = "integration_test"
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        if self.test_cache_name in CACHE:
            del CACHE[self.test_cache_name]
        cache_path = f"data/cache/{self.test_cache_name}.json"
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def test_cache_workflow(self):
        cache = get_cache(self.test_cache_name)

        cache.set("name", "Test User")
        cache.set("score", 100)
        cache.set("active", True)

        self.assertEqual(cache.get("name"), "Test User")
        self.assertEqual(cache.get("score"), 100)
        self.assertEqual(cache.get("active"), True)
        self.assertTrue(cache.exists("name"))
        self.assertFalse(cache.exists("nonexistent"))

        cache.save()

        cache_path = f"data/cache/{self.test_cache_name}.json"
        self.assertTrue(os.path.exists(cache_path))

        cache2 = get_cache(self.test_cache_name)
        self.assertEqual(cache2.get("name"), "Test User")
        self.assertEqual(cache2.get("score"), 100)
        self.assertEqual(cache2.get("active"), True)
