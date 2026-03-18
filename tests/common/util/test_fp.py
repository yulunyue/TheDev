from common.util.fp import File


class TestFp:
    def test_file_operations(self):
        """Test basic file operations"""
        # Test file creation and writing
        test_file = "test_data/temp_test_file.txt"
        f = File.new(test_file)
        
        # Test write_file method
        f.write_file("Hello, World!")
        content = f.read_file()
        
        assert content == "Hello, World!", f"Expected 'Hello, World!', got {content}"
        
        # Test file exists
        assert f.exists(), "File should exist after writing"
        
        # Test file reading different formats
        json_file = File.new("test_data/test.json")
        json_file.write_file({"key": "value", "number": 123})
        json_data = json_file.read_file()
        expected_json = {"key": "value", "number": 123}
        assert json_data == expected_json, f"Expected {expected_json}, got {json_data}"
        
        # Cleanup
        f.remove()
        json_file.remove()
        
        print("✅ File operations test passed")
    
    def test_cache_functionality(self):
        """Test cache functionality"""
        from common.util.fp import get_cache
        
        # Test get_cache
        cache = get_cache("test_cache")
        cache.set("key1", "value1")
        cache.set("key2", {"nested": "data"})
        cache.save()
        
        # Get cache again (should be loaded from disk)
        cache2 = get_cache("test_cache")
        assert cache2.get("key1") == "value1", f"Expected 'value1', got {cache2.get('key1')}"
        assert cache2.get("key2") == {"nested": "data"}, f"Expected nested data, got {cache2.get('key2')}"
        
        print("✅ Cache functionality test passed")


if __name__ == "__main__":
    test_instance = TestFp()
    test_instance.test_file_operations()
    test_instance.test_cache_functionality()
    print("🎉 All tests passed!")
