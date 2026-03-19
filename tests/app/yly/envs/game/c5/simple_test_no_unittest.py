#!/usr/bin/env python3
"""
Simple test to verify c5 module imports and basic functionality - No unittest
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
sys.path.insert(0, project_root)

def assert_equal(actual, expected, message=""):
    """Simple assertion function"""
    if actual != expected:
        print(f"❌ FAIL: {message}")
        print(f"   Expected: {expected}")
        print(f"   Actual: {actual}")
        return False
    print(f"✅ PASS: {message} - {actual}")
    return True

def assert_not_none(actual, message=""):
    """Simple assertion function for not None"""
    if actual is None:
        print(f"❌ FAIL: {message}")
        print(f"   Expected: not None")
        print(f"   Actual: None")
        return False
    print(f"✅ PASS: {message} - {actual}")
    return True

def assert_true(condition, message=""):
    """Simple assertion function for True condition"""
    if not condition:
        print(f"❌ FAIL: {message}")
        print(f"   Expected: True")
        print(f"   Actual: False")
        return False
    print(f"✅ PASS: {message} - True")
    return True

def test_basic_imports():
    """Test basic imports from c5 module"""
    print("🔍 Testing basic imports...")
    
    try:
        # Test submission import
        from app.yly.envs.game.c5.submission import my_controller
        print("✅ submission module imported successfully")
        
        # Test submission function
        result = my_controller({}, {})
        success = assert_equal(result, [], "Submission function result")
        
        return success
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_board_imports():
    """Test board module imports"""
    print("🔍 Testing board module imports...")
    
    try:
        from app.yly.envs.game.c5.board.base import BoardC5
        print("✅ BoardC5 imported successfully")
        
        # Test basic functionality
        board = BoardC5()
        success = assert_true(board.STATE_NULL == 0, "STATE_NULL constant")
        success &= assert_true(board.STATE_FIRST == 1, "STATE_FIRST constant")
        success &= assert_true(board.STATE_SECONED == 2, "STATE_SECONED constant")
        
        # Test loading
        board_loaded = board.load(width=6, height=6, in_row=4)
        success &= assert_equal(board_loaded.size, 36, "Board size 6x6")
        success &= assert_equal(board_loaded.width, 6, "Board width")
        
        return success
        
    except Exception as e:
        print(f"❌ Board import test failed: {e}")
        return False

def test_model_imports():
    """Test model module imports"""
    print("🔍 Testing model module imports...")
    
    try:
        from app.yly.envs.game.c5.model.static_state import StateStatic
        print("✅ StateStatic imported successfully")
        
        # Test static state
        state = StateStatic()
        success = assert_not_none(state, "StateStatic instance")
        success &= assert_equal(StateStatic.init_state, 0, "init_state")
        
        return success
        
    except Exception as e:
        print(f"❌ Model import test failed: {e}")
        return False

def test_player_imports():
    """Test player module imports"""
    print("🔍 Testing player module imports...")
    
    try:
        from app.yly.envs.game.c5.player.al import Al
        from app.yly.envs.game.c5.player.ql import Ql
        from app.yly.envs.game.c5.player.gm_player import GmPlayer
        print("✅ All player modules imported successfully")
        
        # Test player instantiation
        al_player = Al()
        ql_player = Ql()
        gm_player = GmPlayer()
        
        success = assert_not_none(al_player, "Al player")
        success &= assert_not_none(ql_player, "Ql player")
        success &= assert_not_none(gm_player, "Gm player")
        
        return success
        
    except Exception as e:
        print(f"❌ Player import test failed: {e}")
        return False

def test_integration():
    """Test basic integration"""
    print("🔍 Testing basic integration...")
    
    try:
        from app.yly.envs.game.c5.board.base import BoardC5
        from app.yly.envs.game.c5.model.static_state import StateStatic
        from app.yly.envs.game.c5.submission import my_controller
        
        # Set up board
        StateStatic.set_board(width=6, height=6, in_row=4)
        print("✅ Board set up through StateStatic")
        
        # Test submission
        result = my_controller({"test": "data"}, {"action": "space"})
        success = assert_equal(result, [], "Submission function with parameters")
        
        return success
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all simple tests"""
    print("🚀 Starting C5 Module Simple Tests (No Unittest)")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Board Imports", test_board_imports),
        ("Model Imports", test_model_imports),
        ("Player Imports", test_player_imports),
        ("Integration", test_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 Testing {test_name}...")
            success = test_func()
            if success:
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All simple tests passed!")
        return True
    else:
        print("💥 Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)