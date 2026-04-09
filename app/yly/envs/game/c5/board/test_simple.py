#!/usr/bin/env python3
"""
简化的 BoardC5 测试运行器

直接测试 BoardC5 类的核心功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
# 向上找到项目根目录
for i in range(6):
    project_root = os.path.dirname(project_root)

sys.path.insert(0, project_root)

try:
    from app.yly.envs.game.c5.board.base import BoardC5
    print("✅ 成功导入 BoardC5")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("尝试直接导入...")
    # 尝试直接执行
    exec(open('app/yly/envs/game/c5/board/base.py').read())
    BoardC5 = locals().get('BoardC5')
    if BoardC5:
        print("✅ 直接导入成功")
    else:
        print("❌ 无法导入 BoardC5")
        sys.exit(1)


def test_board_creation():
    """测试棋盘创建"""
    print("=== 测试棋盘创建 ===")
    
    # 创建基本棋盘
    board = BoardC5()
    result = board.load(15, 15, 5)
    
    # 验证
    assert result is board, "load 应该返回 self"
    assert board.width == 15, f"width=15, 实际={board.width}"
    assert board.height == 15, f"height=15, 实际={board.height}"
    assert board.in_row == 5, f"in_row=5, 实际={board.in_row}"
    assert board.size == 225, f"size=225, 实际={board.size}"
    
    print("✅ 棋盘创建测试通过")


def test_basic_moves():
    """测试基本落子"""
    print("\n=== 测试基本落子 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 玩家1落子
    board.put_chess(4, 1)  # 中心位置
    assert board.state_pos & board.mask_sets[4], "位置4应该有棋子"
    assert board.state_statu & board.mask_sets[4], "位置4应该是玩家1"
    
    # 玩家2落子
    board.put_chess(1, 2)  # 位置1
    assert board.state_pos & board.mask_sets[1], "位置1应该有棋子"
    assert not (board.state_statu & board.mask_sets[1]), "位置1应该是玩家2"
    
    # 玩家1再次落子
    board.put_chess(2, 1)  # 位置2
    assert board.state_pos & board.mask_sets[2], "位置2应该有棋子"
    assert board.state_statu & board.mask_sets[2], "位置2应该是玩家1"
    
    print("✅ 基本落子测试通过")


def test_board_format():
    """测试棋盘格式化"""
    print("\n=== 测试棋盘格式化 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 空棋盘
    board_str = board.to_str({})
    assert len(board_str) == 4, f"应该有4行，实际有{len(board_str)}行"
    
    # 放置棋子
    board.put_chess(0, 1)  # 玩家1 -> 'O'
    board.put_chess(1, 2)  # 玩家2 -> 'X'
    board.put_chess(4, 1)  # 玩家1 -> 'O'
    
    board_str = board.to_str({})
    board_str_combined = "\n".join(board_str)
    
    assert "O" in board_str_combined, "应该包含 'O'"
    assert "X" in board_str_combined, "应该包含 'X'"
    
    print("✅ 棋盘格式化测试通过")


def test_state_operations():
    """测试状态操作"""
    print("\n=== 测试状态操作 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 设置一些棋子
    board.put_chess(0, 1)
    board.put_chess(1, 2)
    board.put_chess(2, 1)
    
    # 获取状态
    state = board.get_state()
    
    # 创建新棋盘并设置状态
    board2 = BoardC5().load(3, 3, 3)
    board2.set_state(state)
    
    # 验证一致性
    assert board.state_pos == board2.state_pos, "state_pos 应该一致"
    assert board.state_statu == board2.state_statu, "state_statu 应该一致"
    
    print("✅ 状态操作测试通过")


def test_string_conversion():
    """测试字符串转换"""
    print("\n=== 测试字符串转换 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 通过字符串设置状态
    board.change_grid("0|1|2|3|4|5")
    
    # 验证
    for i in range(6):
        assert board.state_pos & board.mask_sets[i], f"位置{i}应该有棋子"
        # 验证玩家交替
        expected_player = (i % 2) + 1
        if expected_player == 1:
            assert board.state_statu & board.mask_sets[i], f"位置{i}应该是玩家1"
        else:
            assert not (board.state_statu & board.mask_sets[i]), f"位置{i}应该是玩家2"
    
    print("✅ 字符串转换测试通过")


def test_chess_removal():
    """测试棋子移除"""
    print("\n=== 测试棋子移除 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 放置棋子
    board.put_chess(4, 1)
    assert board.state_pos & board.mask_sets[4], "位置4应该有棋子"
    
    # 移除棋子
    board.put_chess(4, 0)
    assert not (board.state_pos & board.mask_sets[4]), "位置4应该没有棋子"
    assert not (board.state_statu & board.mask_sets[4]), "位置4应该没有状态"
    
    print("✅ 棋子移除测试通过")


def test_constants():
    """测试常量"""
    print("\n=== 测试常量 ===")
    
    board = BoardC5()
    
    # 验证状态常量
    assert board.STATE_NULL == 0, "STATE_NULL=0"
    assert board.STATE_FIRST == 1, "STATE_FIRST=1"
    assert board.STATE_SECONED == 2, "STATE_SECONED=2"
    
    # 验证方向常量
    expected_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    assert board.DR == expected_directions, f"方向常量错误: {board.DR}"
    
    print("✅ 常量测试通过")


def test_format_function():
    """测试格式化函数"""
    print("\n=== 测试格式化函数 ===")
    
    from app.yly.envs.game.c5.board.base import format
    
    assert format(0) == "-", "format(0) 应该是 '-'"
    assert format(1) == "O", "format(1) 应该是 'O'"
    assert format(2) == "X", "format(2) 应该是 'X'"
    
    # 边界值
    assert format(-1) == "-", "format(-1) 应该是 '-'"
    assert format(3) == "-", "format(3) 应该是 '-'"
    
    print("✅ 格式化函数测试通过")


def main():
    """主函数"""
    print("开始运行 BoardC5 测试...")
    
    try:
        test_board_creation()
        test_basic_moves()
        test_board_format()
        test_state_operations()
        test_string_conversion()
        test_chess_removal()
        test_constants()
        test_format_function()
        
        print("\n🎉 所有测试通过!")
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())