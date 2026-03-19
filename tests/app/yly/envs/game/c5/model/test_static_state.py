#!/usr/bin/env python3
"""
Test cases for c5 static state module - No unittest dependency
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


def test_state_static_initialization():
    """Test StateStatic class initialization"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test class attributes
    success = True
    success &= assert_equal(StateStatic.init_state, 0, "init_state")
    success &= assert_true(hasattr(StateStatic, 'mode'), "Has mode attribute")
    
    # Test creating instance
    state = StateStatic()
    success &= assert_not_none(state, "State instance creation")
    success &= assert_equal(state.state, 0, "Default state value")
    
    return success


def test_set_board_class_method():
    """Test set_board class method"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test setting board with default parameters
    state_class = StateStatic.set_board(6, 6, 4)
    success = assert_not_none(state_class, "set_board return value")
    success &= assert_true(hasattr(StateStatic, 'board'), "Board attribute set")
    
    # Test setting board with custom state
    state_class_with_state = StateStatic.set_board(8, 8, 5, state=1)
    success &= assert_not_none(state_class_with_state, "set_board with state")
    
    return success


def test_set_board_with_instance():
    """Test set_board creates proper board instance"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    from app.yly.envs.game.c5.board.base import BoardC5
    
    # Set up board and check that board is created correctly
    StateStatic.set_board(10, 8, 3)
    
    success = True
    success &= assert_true(hasattr(StateStatic, 'board'), "Board exists")
    success &= assert_true(isinstance(StateStatic.board, BoardC5), "Board is BoardC5 instance")
    success &= assert_equal(StateStatic.board.width, 10, "Board width")
    success &= assert_equal(StateStatic.board.height, 8, "Board height")
    success &= assert_equal(StateStatic.board.in_row, 3, "Board in_row")
    
    return success


def test_reset_method():
    """Test reset method"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Set up board and state
    state_instance = StateStatic.set_board(6, 6, 4, state=5)
    
    # Test reset functionality
    reset_state = state_instance.reset()
    success = assert_not_none(reset_state, "Reset returns state")
    success &= assert_equal(reset_state.state, 5, "Reset preserves state")
    
    return success


def test_state_with_custom_initial_state():
    """Test state creation with custom initial state"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test with different initial states
    success = True
    for initial_state in [0, 1, 2, 10, 100]:
        state = StateStatic(initial_state)
        success &= assert_equal(state.state, initial_state, f"State with initial value {initial_state}")
    
    return success


def test_board_integration():
    """Test integration with BoardC5"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    from app.yly.envs.game.c5.board.base import BoardC5
    
    # Set up board
    StateStatic.set_board(width=5, height=5, in_row=3)
    
    success = True
    success &= assert_true(isinstance(StateStatic.board, BoardC5), "Board is BoardC5")
    success &= assert_equal(StateStatic.board.width, 5, "Board width integration")
    success &= assert_equal(StateStatic.board.height, 5, "Board height integration")
    success &= assert_equal(StateStatic.board.in_row, 3, "Board in_row integration")
    
    return success


def test_static_action_import():
    """Test StaticAction can be imported"""
    from app.yly.envs.game.c5.model.static_action import StaticAction
    
    success = assert_not_none(StaticAction, "StaticAction import")
    
    action = StaticAction()
    success &= assert_not_none(action, "StaticAction instance")
    
    return success


def test_static_action_initialization():
    """Test StaticAction initialization"""
    from app.yly.envs.game.c5.model.static_action import StaticAction
    
    action = StaticAction()
    success = assert_not_none(action, "StaticAction initialization")
    
    return success


def test_dynamic_state_import():
    """Test DynamicState can be imported"""
    from app.yly.envs.game.c5.model.dyn_state import DynamicState
    
    success = assert_not_none(DynamicState, "DynamicState import")
    
    state = DynamicState()
    success &= assert_not_none(state, "DynamicState instance")
    
    return success


def test_dynamic_state_initialization():
    """Test DynamicState initialization"""
    from app.yly.envs.game.c5.model.dyn_state import DynamicState
    
    state = DynamicState()
    success = assert_not_none(state, "DynamicState initialization")
    
    return success


def test_dynamic_action_import():
    """Test DynamicAction can be imported"""
    from app.yly.envs.game.c5.model.dyn_action import DynAction
    
    success = assert_not_none(DynAction, "DynamicAction import")
    
    action = DynAction()
    success &= assert_not_none(action, "DynamicAction instance")
    
    return success


def test_dynamic_action_initialization():
    """Test DynamicAction initialization"""
    from app.yly.envs.game.c5.model.dyn_action import DynAction
    
    action = DynAction()
    success = assert_not_none(action, "DynamicAction initialization")
    
    return success


def test_model_module_imports():
    """Test that all model modules can be imported"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    from app.yly.envs.game.c5.model.static_action import StaticAction
    from app.yly.envs.game.c5.model.dyn_state import DynamicState
    from app.yly.envs.game.c5.model.dyn_action import DynAction
    
    # Test that all classes are properly imported
    success = True
    success &= assert_not_none(StateStatic, "StateStatic import")
    success &= assert_not_none(StaticAction, "StaticAction import")
    success &= assert_not_none(DynamicState, "DynamicState import")
    success &= assert_not_none(DynAction, "DynamicAction import")
    
    return success


def test_state_static_mode_attribute():
    """Test that StateStatic has proper mode attribute"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test that mode is defined
    success = assert_true(hasattr(StateStatic, 'mode'), "Has mode attribute")
    success &= assert_not_none(StateStatic.mode, "Mode is not None")
    
    return success


def run_model_tests():
    """Run all model tests"""
    print("🚀 Starting Model Module Tests")
    print("=" * 50)
    
    tests = [
        ("StateStatic Initialization", test_state_static_initialization),
        ("Set Board Class Method", test_set_board_class_method),
        ("Set Board With Instance", test_set_board_with_instance),
        ("Reset Method", test_reset_method),
        ("State With Custom Initial State", test_state_with_custom_initial_state),
        ("Board Integration", test_board_integration),
        ("Static Action Import", test_static_action_import),
        ("Static Action Initialization", test_static_action_initialization),
        ("Dynamic State Import", test_dynamic_state_import),
        ("Dynamic State Initialization", test_dynamic_state_initialization),
        ("Dynamic Action Import", test_dynamic_action_import),
        ("Dynamic Action Initialization", test_dynamic_action_initialization),
        ("Model Module Imports", test_model_module_imports),
        ("StateStatic Mode Attribute", test_state_static_mode_attribute),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 Testing {test_name}...")
            success = test_func()
            if success:
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Model Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All model tests passed!")
        return True
    else:
        print("💥 Some model tests failed!")
        return False


if __name__ == "__main__":
    success = run_model_tests()
    sys.exit(0 if success else 1)