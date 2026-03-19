#!/usr/bin/env python3
"""
Test script for common.util.tool module
"""
import sys
import os
import random

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from common.util.tool import (
    uid,
    base64_encode,
    ii,
    hash_any_str,
    md5,
    base64_decode,
    b64_code,
    is_base64_code,
)


class TestTool:
    """Test class for common.util.tool functions"""
    
    def expect(self, actual, expected, message=""):
        """Custom assertion method"""
        if actual != expected:
            print(f"❌ FAIL: {message}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {actual}")
            raise AssertionError(f"{message}: Expected {expected}, got {actual}")
        print(f"✅ PASS: {message} - {actual}")

    def test_uid(self):
        """Test uid function"""
        import common.util.tool as tool_module
        
        # Reset the UK_MAP for consistent testing
        tool_module.UK_MAP.clear()
        
        self.expect(uid("a"), "a_0")
        self.expect(uid("a"), "a_1")

    def test_base64(self):
        """Test base64 functions"""
        a = base64_encode("s")
        self.expect(a, "cw==")
        self.expect(base64_decode(a), "s")

        # Test with carriage return (actual function behavior)
        b = base64_encode("a\rc")
        self.expect(b, "YQ1j")
        self.expect(base64_decode(b), "a\rc")

    def test_ii(self):
        """Test integer parsing function"""
        self.expect(ii("2 4  a9 9a 7"), [2, 4, 7])
        self.expect(ii("1 2 3"), [1, 2, 3])

    def test_hash_any(self):
        """Test hash_any_str function"""
        self.expect(hash_any_str("aa"), "aa")
        self.expect(hash_any_str([0, 1, 2]), "012")
        self.expect(hash_any_str(dict(a=1)), "a1")
        
        # Test nested structure
        nested_dict = {"a": 1, "b": {"c": 2}}
        result = hash_any_str(nested_dict)
        self.expect(result, "a1bc2")

    def test_md5(self):
        """Test MD5 hashing function"""
        self.expect(md5("aa"), "4124bc0a9335c27f086f24ba207a4912")
        self.expect(md5("hello"), "5d41402abc4b2a76b9719d911017c592")

    def test_random(self):
        """Test random function"""
        random.seed(0)
        ins = [random.randint(1, 100) for _ in range(10)]
        
        random.seed(0)
        e = [random.randint(1, 100) for _ in range(10)]
        
        self.expect(ins, e)

    def test_additional_functions(self):
        """Test additional functions"""
        # Test b64_code
        encoded = base64_encode("test")
        decoded = b64_code(encoded)
        self.expect(decoded, "test")
        
        # Test is_base64_code
        self.expect(is_base64_code("aGVsbG8="), True)
        self.expect(is_base64_code("invalid"), False)


def run_tests():
    """Run all test methods"""
    print("🚀 Starting test_util_tool.py tests...\n")
    
    test_instance = TestTool()
    tests = [
        ("UID", test_instance.test_uid),
        ("Base64", test_instance.test_base64),
        ("Integer Parsing", test_instance.test_ii),
        ("Hash Any String", test_instance.test_hash_any),
        ("MD5", test_instance.test_md5),
        ("Random", test_instance.test_random),
        ("Additional Functions", test_instance.test_additional_functions),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"🔍 Testing {test_name}...")
            test_func()
            passed += 1
            print()
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}\n")
            import traceback
            traceback.print_exc()
            print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All test_util_tool.py tests passed!")
        return True
    else:
        print("💥 Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)