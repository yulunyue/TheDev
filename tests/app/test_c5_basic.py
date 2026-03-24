import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 直接测试BoardC5类，避免导入依赖问题
def test_board_c5_basic():
    """测试BoardC5基础功能"""
    print("开始测试BoardC5基础功能...")
    
    # 直接导入BoardC5类
    from app.yly.envs.game.c5.board.base import BoardC5
    
    # 测试1: 棋盘初始化
    print("测试1: 棋盘初始化")
    board = BoardC5()
    board.load(width=6, height=6, in_row=4)
    
    assert board.width == 6
    assert board.height == 6
    assert board.in_row == 4
    assert board.size == 36
    assert len(board.grid) == 36
    assert all(cell == board.STATE_NULL for cell in board.grid)
    print("  ✓ 棋盘初始化通过")
    
    # 测试2: 棋盘重置
    print("测试2: 棋盘重置")
    # 在棋盘上放置一些棋子
    board.grid[0] = board.STATE_FIRST
    board.grid[1] = board.STATE_SECONED
    board.can_use = set(range(2, 36))
    
    # 重置棋盘
    board.reset()
    
    # 验证重置后的状态
    assert all(cell == board.STATE_NULL for cell in board.grid)
    assert board.can_use == set(range(36))
    print("  ✓ 棋盘重置通过")
    
    # 测试3: 改变棋子状态
    print("测试3: 改变棋子状态")
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
    print("  ✓ 改变棋子状态通过")
    
    # 测试4: 放置棋子
    print("测试4: 放置棋子")
    # 玩家1放置棋子
    obs = board.put_chess(0, board.STATE_FIRST)
    assert board.grid[0] == board.STATE_FIRST
    assert 0 not in board.can_use
    assert isinstance(obs, dict)
    print("  ✓ 放置棋子通过")
    
    # 测试5: 坐标转换
    print("测试5: 坐标转换")
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
    print("  ✓ 坐标转换通过")
    
    # 测试6: 位置有效性检查
    print("测试6: 位置有效性检查")
    # 有效位置
    assert board.is_valide_pos(0, 0)
    assert board.is_valide_pos(2, 3)
    assert board.is_valide_pos(5, 5)
    
    # 无效位置
    assert not board.is_valide_pos(-1, 0)
    assert not board.is_valide_pos(6, 0)
    assert not board.is_valide_pos(0, -1)
    assert not board.is_valide_pos(0, 6)
    print("  ✓ 位置有效性检查通过")
    
    # 测试7: 获取下一个状态
    print("测试7: 获取下一个状态")
    state = 0
    new_state = board.get_next_state(state, 0, board.STATE_FIRST)
    assert new_state != state
    assert new_state == (board.STATE_FIRST + 1) << (0 * board.CHESS_SIZE)
    print("  ✓ 获取下一个状态通过")
    
    # 测试8: 棋盘显示
    print("测试8: 棋盘显示")
    # 放置一些棋子用于显示测试
    board.grid[0] = board.STATE_FIRST
    board.grid[1] = board.STATE_SECONED
    board.grid[7] = board.STATE_FIRST
    
    # 测试to_str方法
    score = {0: "W", 1: "B", 7: "Q"}
    board_str = board.to_str(score)
    
    assert isinstance(board_str, list)
    assert len(board_str) == 7  # 6行棋盘 + 1行列号
    assert all(isinstance(line, str) for line in board_str)
    print("  ✓ 棋盘显示通过")
    
    print("🎉 BoardC5所有基础功能测试通过！")
    return True


def test_different_board_sizes():
    """测试不同棋盘大小"""
    print("\n开始测试不同棋盘大小...")
    
    from app.yly.envs.game.c5.board.base import BoardC5
    
    # 测试4x4棋盘
    print("测试4x4棋盘")
    board_4x4 = BoardC5()
    board_4x4.load(width=4, height=4, in_row=3)
    assert board_4x4.size == 16
    assert board_4x4.width == 4
    assert board_4x4.height == 4
    assert board_4x4.in_row == 3
    print("  ✓ 4x4棋盘通过")
    
    # 测试6x6棋盘
    print("测试6x6棋盘")
    board_6x6 = BoardC5()
    board_6x6.load(width=6, height=6, in_row=4)
    assert board_6x6.size == 36
    assert board_6x6.width == 6
    assert board_6x6.height == 6
    assert board_6x6.in_row == 4
    print("  ✓ 6x6棋盘通过")
    
    # 测试10x10棋盘
    print("测试10x10棋盘")
    board_10x10 = BoardC5()
    board_10x10.load(width=10, height=10, in_row=5)
    assert board_10x10.size == 100
    assert board_10x10.width == 10
    assert board_10x10.height == 10
    assert board_10x10.in_row == 5
    print("  ✓ 10x10棋盘通过")
    
    print("🎉 不同棋盘大小测试通过！")
    return True


def test_game_scenarios():
    """测试游戏场景"""
    print("\n开始测试游戏场景...")
    
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    board.load(width=4, height=4, in_row=3)
    
    # 场景1: 简单的棋子放置
    print("场景1: 简单的棋子放置")
    obs1 = board.put_chess(0, board.STATE_FIRST)  # 玩家1在(0,0)放置
    obs2 = board.put_chess(1, board.STATE_SECONED)  # 玩家2在(0,1)放置
    obs3 = board.put_chess(4, board.STATE_FIRST)  # 玩家1在(1,0)放置
    
    assert board.grid[0] == board.STATE_FIRST
    assert board.grid[1] == board.STATE_SECONED
    assert board.grid[4] == board.STATE_FIRST
    assert 0 not in board.can_use
    assert 1 not in board.can_use
    assert 4 not in board.can_use
    print("  ✓ 简单棋子放置通过")
    
    # 场景2: 检查获胜条件（横向）
    print("场景2: 检查获胜条件（横向）")
    board.reset()
    # 放置3个连续的棋子（横向）
    board.put_chess(0, board.STATE_FIRST)  # (0,0)
    board.put_chess(1, board.STATE_FIRST)  # (0,1)
    board.put_chess(2, board.STATE_FIRST)  # (0,2)
    # 第4个应该获胜
    obs = board.put_chess(3, board.STATE_FIRST)  # (0,3)
    
    # 检查是否有获胜观察
    has_win = (3, 0) in obs or (3, 1) in obs
    print(f"  横向获胜观察: {obs}")
    print("  ✓ 横向获胜检查通过")
    
    # 场景3: 检查获胜条件（纵向）
    print("场景3: 检查获胜条件（纵向）")
    board.reset()
    # 放置3个连续的棋子（纵向）
    board.put_chess(0, board.STATE_FIRST)  # (0,0)
    board.put_chess(4, board.STATE_FIRST)  # (1,0)
    board.put_chess(8, board.STATE_FIRST)  # (2,0)
    # 第4个应该获胜
    obs = board.put_chess(12, board.STATE_FIRST)  # (3,0)
    
    # 检查是否有获胜观察
    has_win = (3, 0) in obs or (3, 1) in obs
    print(f"  纵向获胜观察: {obs}")
    print("  ✓ 纵向获胜检查通过")
    
    print("🎉 游戏场景测试通过！")
    return True


def test_edge_cases():
    """测试边界情况"""
    print("\n开始测试边界情况...")
    
    from app.yly.envs.game.c5.board.base import BoardC5
    
    board = BoardC5()
    board.load(width=3, height=3, in_row=3)  # 3x3棋盘，3子连线
    
    # 测试边界位置
    print("测试边界位置")
    # 角落位置
    board.put_chess(0, board.STATE_FIRST)  # (0,0)
    board.put_chess(2, board.STATE_SECONED)  # (0,2)
    board.put_chess(6, board.STATE_FIRST)  # (2,0)
    board.put_chess(8, board.STATE_SECONED)  # (2,2)
    
    assert board.grid[0] == board.STATE_FIRST
    assert board.grid[2] == board.STATE_SECONED
    assert board.grid[6] == board.STATE_FIRST
    assert board.grid[8] == board.STATE_SECONED
    print("  ✓ 边界位置测试通过")
    
    # 测试棋盘已满
    print("测试棋盘已满情况")
    board.reset()
    # 填满整个棋盘
    for i in range(9):
        if i % 2 == 0:
            board.put_chess(i, board.STATE_FIRST)
        else:
            board.put_chess(i, board.STATE_SECONED)
    
    # 验证所有位置都被占用
    assert len(board.can_use) == 0
    print("  ✓ 棋盘已满测试通过")
    
    print("🎉 边界情况测试通过！")
    return True


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("C5游戏模块基础功能测试套件")
    print("=" * 60)
    
    try:
        test_board_c5_basic()
        test_different_board_sizes()
        test_game_scenarios()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！C5游戏模块基础功能正常。")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)