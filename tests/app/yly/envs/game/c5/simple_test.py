#!/usr/bin/env python3
"""
Simple test to verify c5 module imports and basic functionality
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
sys.path.insert(0, project_root)

def test_basic_imports():
    """Test basic imports from c5 module"""
    print("🔍 Testing basic imports...")
    
    try:
        # Test submission import
        from app.yly.envs.game.c5.submission import my_controller
        print("✅ submission module imported successfully")
        
        # Test submission function
        result = my_controller({}, {})
        print(f"✅ submission function works: {result}")
        
        return True
        
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
        print(f"✅ BoardC5 instantiated: constants={board.STATE_NULL}, {board.STATE_FIRST}, {board.STATE_SECONED}")
        
        # Test loading
        board_loaded = board.load(width=6, height=6, in_row=4)
        print(f"✅ Board loaded: size={board_loaded.size}, width={board_loaded.width}")
        
        return True
        
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
        print(f"✅ StateStatic instantiated: init_state={StateStatic.init_state}")
        
        return True
        
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
        
        print("✅ All players instantiated successfully")
        return True
        
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
        print(f"✅ Submission function works with parameters: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all simple tests"""
    print("🚀 Starting C5 Module Simple Tests")
    print("=" * 50)
    
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
    
    print("\n" + "=" * 50)
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