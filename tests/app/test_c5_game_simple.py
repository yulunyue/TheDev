import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.yly.envs.game.c5.board.base import BoardC5
from app.yly.envs.game.c5.model.static_state import StateStatic
from app.yly.envs.game.c5.model.static_action import C5ACtion


def test_board_initialization():
    """测试棋盘初始化"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    assert board.width == 6
    assert board.height == 6
    assert board.in_row == 4
    assert board.size == 36
    assert len(board.grid) == 36
    assert all(cell == board.STATE_NULL for cell in board.grid)
    print("✓ 棋盘初始化测试通过")


def test_board_reset():
    """测试棋盘重置"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    # 在棋盘上放置一些棋子
    board.grid[0] = board.STATE_FIRST
    board.grid[1] = board.STATE_SECONED
    board.can_use = set(range(2, 36))
    
    # 重置棋盘
    board.reset()
    
    # 验证重置后的状态
    assert all(cell == board.STATE_NULL for cell in board.grid)
    assert board.can_use == set(range(36))
    print("✓ 棋盘重置测试通过")


def test_change_chess_status():
    """测试改变棋子状态"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    # 测试玩家1放置棋子
    board.change_chess_statu(0, board.STATE_FIRST)
    assert board.grid[0] == board.STATE_FIRST
    assert 0 not in board.can_use
    
    # 测试玩家2放置棋子
    board.change_chess_statu(1, board.STATE_SECONED)
    assert board.grid[1] == board.STATE_SECONED
    assert 1 not in board.can_use
    
    # 测试移除棋子（设置为空）
    board.change_chess_statu(0, board.STATE_NULL)
    assert board.grid[0] == board.STATE_NULL
    assert 0 in board.can_use
    print("✓ 改变棋子状态测试通过")


def test_put_chess():
    """测试放置棋子"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    # 玩家1放置棋子
    obs = board.put_chess(0, board.STATE_FIRST)
    assert board.grid[0] == board.STATE_FIRST
    assert 0 not in board.can_use
    assert isinstance(obs, dict)
    print("✓ 放置棋子测试通过")


def test_get_yx_and_get_idx():
    """测试坐标转换"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    # 测试get_yx方法
    y, x = board.get_yx(0)
    assert y == 0, x == 0
    
    y, x = board.get_yx(35)
    assert y == 5, x == 5
    
    y, x = board.get_yx(7)
    assert y == 1, x == 1
    
    # 测试get_idx方法
    idx = board.get_idx(0, 0)
    assert idx == 0
    
    idx = board.get_idx(5, 5)
    assert idx == 35
    
    idx = board.get_idx(1, 1)
    assert idx == 7
    print("✓ 坐标转换测试通过")


def test_is_valid_position():
    """测试位置有效性检查"""
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    # 有效位置
    assert board.is_valide_pos(0, 0)
    assert board.is_valide_pos(2, 3)
    assert board.is_valide_pos(5, 5)
    
    # 无效位置
    assert not board.is_valide_pos(-1, 0)
    assert not board.is_valide_pos(6, 0)
    assert not board.is_valide_pos(0, -1)
    assert not board.is_valide_pos(0, 6)
    print("✓ 位置有效性检查测试通过")


def test_state_initialization():
    """测试状态初始化"""
    state_class = StateStatic
    state_class.set_board(6, 6, 4)
    state = state_class()
    
    assert state.state == 0
    assert state.depth == 0
    assert state.player_id == 0
    assert state.can_moves == list(range(36))
    assert state.done is None
    print("✓ 状态初始化测试通过")


def test_set_state_integer():
    """测试设置整数状态"""
    state_class = StateStatic
    state_class.set_board(6, 6, 4)
    state = state_class()
    
    state_value = 15  # 二进制: 1111
    state.set_state(state_value)
    
    assert state.state == state_value
    assert state.depth == 4  # 4个棋子
    assert state.player_id == 0  # 偶数深度，玩家1
    assert state.can_moves == list(range(36))  # 所有位置都可用
    print("✓ 设置整数状态测试通过")


def test_get_action():
    """测试获取动作"""
    state_class = StateStatic
    state_class.set_board(6, 6, 4)
    state = state_class()
    
    pos = 0
    action = state.get_action(pos)
    
    assert isinstance(action, C5ACtion)
    assert action.action == pos
    assert action.src == state
    assert action.dst.player_id == 1  # 下一个玩家
    assert action.dst.depth == 1  # 深度加1
    print("✓ 获取动作测试通过")


def test_make_actions():
    """测试生成所有可能的动作"""
    state_class = StateStatic
    state_class.set_board(6, 6, 4)
    state = state_class()
    
    actions = state.make_actions()
    
    assert len(actions) == 36  # 6x6棋盘，36个位置
    assert all(isinstance(action, C5ACtion) for action in actions)
    assert all(action.src == state for action in actions)
    print("✓ 生成所有可能动作测试通过")


def test_action_initialization():
    """测试动作初始化"""
    state_class = StateStatic
    state_class.set_board(6, 6, 4)
    src_state = state_class()
    action = src_state.get_action(0)
    
    assert action.src == src_state
    assert action.action == 0
    assert action.obs is None
    assert action.reward == 0
    assert action.dst is not None
    print("✓ 动作初始化测试通过")


def test_simple_game_flow():
    """测试简单游戏流程"""
    state_class = StateStatic
    state_class.set_board(4, 4, 3)  # 4x4棋盘，3子连线
    
    state = state_class()
    
    # 玩家1放置棋子
    action1 = state.get_action(0)
    assert action1.src.player_id == 0  # 玩家1
    
    # 玩家2放置棋子
    state = action1.dst
    action2 = state.get_action(1)
    assert action2.src.player_id == 1  # 玩家2
    
    # 验证状态转移
    assert action1.dst == action2.src
    print("✓ 简单游戏流程测试通过")


def test_board_state_consistency():
    """测试棋盘和状态的一致性"""
    state_class = StateStatic
    state_class.set_board(4, 4, 3)  # 4x4棋盘，3子连线
    
    state = state_class()
    
    # 获取动作并执行
    action = state.get_action(5)
    new_state = action.dst
    
    # 验证状态转移正确
    assert new_state.depth == state.depth + 1
    assert new_state.player_id == 1 - state.player_id
    
    # 验证棋盘状态
    assert new_state.state != state.state
    print("✓ 棋盘和状态一致性测试通过")


def run_all_tests():
    """运行所有测试"""
    print("开始运行C5游戏模块测试...")
    print("=" * 50)
    
    try:
        test_board_initialization()
        test_board_reset()
        test_change_chess_status()
        test_put_chess()
        test_get_yx_and_get_idx()
        test_is_valid_position()
        test_state_initialization()
        test_set_state_integer()
        test_get_action()
        test_make_actions()
        test_action_initialization()
        test_simple_game_flow()
        test_board_state_consistency()
        
        print("=" * 50)
        print("🎉 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)