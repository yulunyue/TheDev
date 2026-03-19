#!/usr/bin/env python3
"""
Integration tests for c5 game module - No unittest dependency
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


def test_full_game_setup():
    """Test setting up a complete c5 game"""
    from app.yly.envs.game.c5.board.base import BoardC5
    from app.yly.envs.game.c5.model.static_state import StateStatic
    from app.yly.envs.game.c5.player.al import Al
    from app.yly.envs.game.c5.player.ql import Ql
    from app.yly.envs.game.c5.player.gm_player import GmPlayer
    
    # Set up game board
    StateStatic.set_board(width=6, height=6, in_row=4)
    
    # Create players
    al_player = Al()
    ql_player = Ql()
    gm_player = GmPlayer()
    
    # Verify all components are working together
    success = True
    success &= assert_not_none(StateStatic.board, "Board exists")
    success &= assert_equal(StateStatic.board.width, 6, "Board width")
    success &= assert_equal(StateStatic.board.height, 6, "Board height")
    success &= assert_equal(StateStatic.board.in_row, 4, "Board in_row")
    
    success &= assert_not_none(al_player, "Al player")
    success &= assert_not_none(ql_player, "Ql player")
    success &= assert_not_none(gm_player, "Gm player")
    
    return success


def test_submission_function():
    """Test the submission function"""
    from app.yly.envs.game.c5.submission import my_controller
    
    # Test with different observation and action space parameters
    observation = {}
    action_space = {}
    
    # Test default call
    result = my_controller(observation, action_space)
    success = assert_equal(result, [], "Default submission result")
    success &= assert_true(isinstance(result, list), "Result is list")
    
    # Test with continuous action space
    result_continuous = my_controller(observation, action_space, is_act_continuous=True)
    success &= assert_equal(result_continuous, [], "Continuous submission result")
    success &= assert_true(isinstance(result_continuous, list), "Continuous result is list")
    
    return success


def test_board_state_integration():
    """Test integration between board and state"""
    from app.yly.envs.game.c5.board.base import BoardC5
    from app.yly.envs.game.c5.board.base_state import BoardC5State
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Create board and state
    board = BoardC5().load(width=8, height=8, in_row=3)
    state = BoardC5State(value=42)
    
    # Set up static state with board
    StateStatic.set_board(width=8, height=8, in_row=3)
    
    # Verify integration
    success = True
    success &= assert_equal(board.size, 64, "Board size 8x8")
    success &= assert_equal(state.value, 42, "State value")
    success &= assert_equal(StateStatic.board.width, 8, "Static board width")
    success &= assert_equal(StateStatic.board.height, 8, "Static board height")
    
    return success


def test_player_diversity():
    """Test that we have different types of players"""
    from app.yly.envs.game.c5.player.al import Al
    from app.yly.envs.game.c5.player.ql import Ql
    from app.yly.envs.game.c5.player.gm_player import GmPlayer
    
    # Create players
    players = {
        'al': Al(),
        'ql': Ql(),
        'gm': GmPlayer()
    }
    
    # Verify all players are different instances
    success = True
    success &= assert_true(players['al'] is not players['ql'], "Al and Ql are different")
    success &= assert_true(players['ql'] is not players['gm'], "Ql and Gm are different")
    success &= assert_true(players['al'] is not players['gm'], "Al and Gm are different")
    
    # All should be valid player instances
    for name, player in players.items():
        success &= assert_not_none(player, f"{name} player exists")
        success &= assert_true(hasattr(player, '__init__'), f"{name} has __init__")
    
    return success


def test_game_constants_consistency():
    """Test that game constants are consistent across modules"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    
    # Test that board constants are reasonable
    success = True
    success &= assert_true(board.BIT_SIZE > 0, "BIT_SIZE > 0")
    success &= assert_true(board.CHESS_SIZE > 0, "CHESS_SIZE > 0")
    success &= assert_equal(len(board.DR), 4, "Number of directions")
    
    # Test direction vectors are valid
    for dr in board.DR:
        success &= assert_equal(len(dr), 2, f"Direction length: {dr}")
        success &= assert_true(isinstance(dr[0], int), f"Direction x type: {dr}")
        success &= assert_true(isinstance(dr[1], int), f"Direction y type: {dr}")
    
    return success


def test_state_modes():
    """Test state modes and their properties"""
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test that static state has proper mode
    success = True
    success &= assert_true(hasattr(StateStatic, 'mode'), "Has mode attribute")
    success &= assert_not_none(StateStatic.mode, "Mode is not None")
    success &= assert_equal(StateStatic.init_state, 0, "Init state is 0")
    
    return success


def test_board_dimensions_variations():
    """Test board with different dimensions"""
    from app.yly.envs.game.c5.board.base import BoardC5
    from app.yly.envs.game.c5.model.static_state import StateStatic
    
    # Test various board sizes
    test_dimensions = [
        (6, 6, 4),   # Standard
        (8, 8, 5),   # Larger board
        (10, 10, 5), # Even larger
        (4, 4, 3),   # Smaller board
    ]
    
    success = True
    for width, height, in_row in test_dimensions:
        # Test board directly
        board = BoardC5().load(width=width, height=height, in_row=in_row)
        success &= assert_equal(board.width, width, f"Board width {width}x{height}")
        success &= assert_equal(board.height, height, f"Board height {width}x{height}")
        success &= assert_equal(board.in_row, in_row, f"Board in_row {width}x{height}")
        success &= assert_equal(board.size, width * height, f"Board size {width}x{height}")
        
        # Test through static state
        StateStatic.set_board(width=width, height=height, in_row=in_row)
        success &= assert_equal(StateStatic.board.width, width, f"Static board width {width}x{height}")
        success &= assert_equal(StateStatic.board.height, height, f"Static board height {width}x{height}")
        success &= assert_equal(StateStatic.board.in_row, in_row, f"Static board in_row {width}x{height}")
    
    return success


def test_c5_module_completeness():
    """Test that c5 module is complete and functional"""
    # Test importing all main components
    from app.yly.envs.game.c5.board.base import BoardC5
    from app.yly.envs.game.c5.board.base_state import BoardC5State
    from app.yly.envs.game.c5.model.static_state import StateStatic
    from app.yly.envs.game.c5.model.static_action import StaticAction
    from app.yly.envs.game.c5.model.dyn_state import DynamicState
    from app.yly.envs.game.c5.model.dyn_action import DynAction
    from app.yly.envs.game.c5.player.al import Al
    from app.yly.envs.game.c5.player.ql import Ql
    from app.yly.envs.game.c5.player.gm_player import GmPlayer
    from app.yly.envs.game.c5.submission import my_controller
    
    # Test that all components can be instantiated
    board = BoardC5()
    board_state = BoardC5State()
    static_state = StateStatic()
    static_action = StaticAction()
    dynamic_state = DynamicState()
    dynamic_action = DynAction()
    al_player = Al()
    ql_player = Ql()
    gm_player = GmPlayer()
    
    # Test submission function
    result = my_controller({}, {})
    
    # Verify all are not None
    components = [
        board, board_state, static_state, static_action,
        dynamic_state, dynamic_action, al_player, ql_player, gm_player
    ]
    
    success = True
    for component in components:
        success &= assert_not_none(component, "Component exists")
    
    success &= assert_equal(result, [], "Submission result")
    
    return success


def test_c5_game_rules_consistency():
    """Test that game rules are consistent"""
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    
    # Test win condition directions
    directions = board.DR
    expected_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    
    success = assert_equal(directions, expected_directions, "Direction vectors")
    
    # Test that these directions make sense for a 5-in-a-row game
    # [0,1] = horizontal, [1,0] = vertical, [1,1] = diagonal down-right, [1,-1] = diagonal down-left
    
    return success


def run_integration_tests():
    """Run all integration tests"""
    print("🚀 Starting C5 Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Full Game Setup", test_full_game_setup),
        ("Submission Function", test_submission_function),
        ("Board State Integration", test_board_state_integration),
        ("Player Diversity", test_player_diversity),
        ("Game Constants Consistency", test_game_constants_consistency),
        ("State Modes", test_state_modes),
        ("Board Dimensions Variations", test_board_dimensions_variations),
        ("C5 Module Completeness", test_c5_module_completeness),
        ("C5 Game Rules Consistency", test_c5_game_rules_consistency),
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
    
    print(f"\n📊 Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("💥 Some integration tests failed!")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)