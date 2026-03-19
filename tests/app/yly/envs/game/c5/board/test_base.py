#!/usr/bin/env python3
"""
Test cases for c5 board module - No unittest dependency
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


def test_board_initialization():
    """Test board initialization with default parameters"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    
    # Test default constants
    success = True
    success &= assert_equal(board.STATE_NULL, 0, "STATE_NULL")
    success &= assert_equal(board.STATE_FIRST, 1, "STATE_FIRST") 
    success &= assert_equal(board.STATE_SECONED, 2, "STATE_SECONED")
    success &= assert_equal(board.BIT_SIZE, 2, "BIT_SIZE")
    success &= assert_equal(board.CHESS_SIZE, 2, "CHESS_SIZE")
    success &= assert_equal(board.DR, [[0, 1], [1, 0], [1, 1], [1, -1]], "Direction vectors")
    
    return success


def test_board_load_default():
    """Test board loading with default parameters"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5().load()
    
    success = True
    success &= assert_equal(board.width, 6, "Default width")
    success &= assert_equal(board.height, 6, "Default height")
    success &= assert_equal(board.in_row, 4, "Default in_row")
    success &= assert_true(not board.just_for_view, "Default view mode")
    success &= assert_equal(board.size, 36, "Default size")  # 6 * 6
    
    return success


def test_board_load_custom():
    """Test board loading with custom parameters"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5().load(width=8, height=8, in_row=5)
    
    success = True
    success &= assert_equal(board.width, 8, "Custom width")
    success &= assert_equal(board.height, 8, "Custom height")
    success &= assert_equal(board.in_row, 5, "Custom in_row")
    success &= assert_equal(board.size, 64, "Custom size")  # 8 * 8
    
    return success


def test_board_view_mode():
    """Test board view mode"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5().load(just_for_view=True)
    
    success = assert_true(board.just_for_view, "View mode enabled")
    return success


def test_init_size():
    """Test size initialization"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5().load(width=10, height=5)
    success = assert_equal(board.size, 50, "Size calculation 10x5")  # 10 * 5
    
    # Test with different dimensions
    board.load(width=5, height=10)
    success &= assert_equal(board.size, 50, "Size calculation 5x10")  # 5 * 10
    
    return success


def test_board_constants_consistency():
    """Test that board constants are consistent"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    
    # Test that constants are properly defined
    success = True
    success &= assert_true(hasattr(board, 'STATE_NULL'), "Has STATE_NULL")
    success &= assert_true(hasattr(board, 'STATE_FIRST'), "Has STATE_FIRST")
    success &= assert_true(hasattr(board, 'STATE_SECONED'), "Has STATE_SECONED")
    success &= assert_true(hasattr(board, 'BIT_SIZE'), "Has BIT_SIZE")
    success &= assert_true(hasattr(board, 'CHESS_SIZE'), "Has CHESS_SIZE")
    success &= assert_true(hasattr(board, 'DR'), "Has DR")
    
    # Test direction vectors
    directions = board.DR
    success &= assert_equal(len(directions), 4, "Number of directions")
    success &= assert_equal(directions[0], [0, 1], "Right direction")
    success &= assert_equal(directions[1], [1, 0], "Down direction")
    success &= assert_equal(directions[2], [1, 1], "Diagonal down-right")
    success &= assert_equal(directions[3], [1, -1], "Diagonal down-left")
    
    return success


def test_board_state_initialization():
    """Test board state initialization"""
    from app.yly.envs.game.c5.board.base_state import BoardC5State
    
    # Test basic state creation
    state = BoardC5State()
    success = assert_not_none(state, "Basic state creation")
    
    # Test state with initial value
    state_with_value = BoardC5State(value=5)
    success &= assert_equal(state_with_value.value, 5, "State with initial value")
    
    return success


def test_board_state_properties():
    """Test board state properties"""
    from app.yly.envs.game.c5.board.base_state import BoardC5State
    
    state = BoardC5State()
    
    # Test that state has expected properties
    success = True
    success &= assert_true(hasattr(state, 'value'), "Has value property")
    success &= assert_true(hasattr(state, 'board'), "Has board property")
    
    # Test value setting and getting
    state.value = 10
    success &= assert_equal(state.value, 10, "Value setting and getting")
    
    return success


def test_board_imports():
    """Test that all board modules can be imported"""
    from app.yly.envs.game.c5.board.base import BoardC5
    from app.yly.envs.game.c5.board.base_state import BoardC5State
    
    # Test that classes are properly imported
    success = True
    success &= assert_not_none(BoardC5, "BoardC5 import")
    success &= assert_not_none(BoardC5State, "BoardC5State import")
    
    return success


def run_board_tests():
    """Run all board tests"""
    print("🚀 Starting Board Module Tests")
    print("=" * 50)
    
    tests = [
        ("Board Initialization", test_board_initialization),
        ("Board Load Default", test_board_load_default),
        ("Board Load Custom", test_board_load_custom),
        ("Board View Mode", test_board_view_mode),
        ("Init Size", test_init_size),
        ("Board Constants Consistency", test_board_constants_consistency),
        ("Board State Initialization", test_board_state_initialization),
        ("Board State Properties", test_board_state_properties),
        ("Board Imports", test_board_imports),
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
    
    print(f"\n📊 Board Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All board tests passed!")
        return True
    else:
        print("💥 Some board tests failed!")
        return False


if __name__ == "__main__":
    success = run_board_tests()
    sys.exit(0 if success else 1)