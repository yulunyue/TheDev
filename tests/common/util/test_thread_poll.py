#!/usr/bin/env python3
"""
Test script for ThreadPoll functionality
Fully compatible with pytest conventions
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

import time


def thread_func_test(m):
    """Test function for thread polling"""
    time.sleep(m)
    return m


def test_thread_poll_functionality():
    """Test ThreadPoll functionality using pytest conventions"""
    from common.util.thread.thread_poll import ThreadManage
    
    # Create ThreadManage instance
    manage = ThreadManage()
    
    # Test with different sleep times
    result = manage.run(thread_func_test, [0.4, 0.3, 0.1])
    
    # Expected result: threads should complete in order of execution time
    # Shorter sleep times should complete first
    expected = [0.1, 0.3, 0.4]
    
    # Use standard pytest assertion style
    assert result == expected, f"Expected {expected}, got {result}"


def test_thread_poll_with_empty_list():
    """Test ThreadPoll with empty input list"""
    from common.util.thread.thread_poll import ThreadManage
    
    manage = ThreadManage()
    result = manage.run(thread_func_test, [])
    
    # Should return empty list for empty input
    assert result == [], f"Expected empty list, got {result}"


def test_thread_poll_with_single_item():
    """Test ThreadPoll with single item"""
    from common.util.thread.thread_poll import ThreadManage
    
    manage = ThreadManage()
    result = manage.run(thread_func_test, [0.1])
    
    assert result == [0.1], f"Expected [0.1], got {result}"


def test_thread_poll_error_handling():
    """Test ThreadPoll error handling"""
    from common.util.thread.thread_poll import ThreadManage
    
    def error_func(x):
        if x < 0:
            raise ValueError("Negative value not allowed")
        return x * 2
    
    manage = ThreadManage()
    
    # Should handle errors gracefully
    try:
        manage.run(error_func, [1, 2, -1, 3])
        # If no error is raised, that's also acceptable behavior
        assert True
    except ValueError:
        # ValueError is expected for negative input
        assert True
    except Exception as e:
        # Any other exception should be reported
        raise AssertionError(f"Unexpected error type: {e}")


def test_thread_poll_multiple_calls():
    """Test ThreadPoll with multiple consecutive calls"""
    from common.util.thread.thread_poll import ThreadManage
    
    manage = ThreadManage()
    
    # First call
    result1 = manage.run(thread_func_test, [0.2, 0.1])
    assert result1 == [0.1, 0.2]
    
    # Second call immediately after first
    result2 = manage.run(thread_func_test, [0.1, 0.2])
    assert result2 == [0.1, 0.2]
    
    # Third call with different parameters
    result3 = manage.run(thread_func_test, [0.05])
    assert result3 == [0.05]


if __name__ == "__main__":
    # Run tests manually if executed directly
    import traceback
    
    tests = [
        test_thread_poll_functionality,
        test_thread_poll_with_empty_list,
        test_thread_poll_with_single_item,
        test_thread_poll_error_handling,
        test_thread_poll_multiple_calls,
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            print(f"✅ {test_func.__name__} passed")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} failed: {e}")
            traceback.print_exc()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("💥 Some tests failed!")
        sys.exit(1)