#!/usr/bin/env python3
"""
BoardC5 测试运行器

运行 BoardC5 类的所有测试
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
sys.path.insert(0, project_root)

from app.yly.envs.game.c5.board.base import BoardC5


def test_basic_initialization():
    """测试基本棋盘初始化"""
    print("=== 测试基本棋盘初始化 ===")
    
    board = BoardC5()
    result = board.load(15, 15, 5)
    
    # 验证返回对象
    assert result is board, "load 方法应该返回 self"
    
    # 验证属性设置
    assert board.width == 15, f"width 应该是 15，实际是 {board.width}"
    assert board.height == 15, f"height 应该是 15，实际是 {board.height}"
    assert board.in_row == 5, f"in_row 应该是 5，实际是 {board.in_row}"
    assert board.size == 225, f"size 应该是 225，实际是 {board.size}"
    
    # 验证掩码设置
    assert board.mask_h == (1 << 15) - 1, f"mask_h 计算错误"
    assert board.mask_full == (1 << 225) - 1, f"mask_full 计算错误"
    
    # 验证初始状态
    assert board.state_pos == 0, f"state_pos 应该是 0，实际是 {board.state_pos}"
    assert board.state_statu == 0, f"state_statu 应该是 0，实际是 {board.state_statu}"
    
    print("✅ 基本初始化测试通过")


def test_minimal_board():
    """测试最小棋盘"""
    print("\n=== 测试最小棋盘 ===")
    
    board = BoardC5()
    board.load(3, 3, 3)
    
    assert board.width == 3, f"width 应该是 3，实际是 {board.width}"
    assert board.height == 3, f"height 应该是 3，实际是 {board.height}"
    assert board.in_row == 3, f"in_row 应该是 3，实际是 {board.in_row}"
    assert board.size == 9, f"size 应该是 9，实际是 {board.size}"
    assert board.mask_h == (1 << 3) - 1, f"mask_h 计算错误"
    assert board.mask_full == (1 << 9) - 1, f"mask_full 计算错误"
    
    print("✅ 最小棋盘测试通过")


def test_put_chess():
    """测试落子操作"""
    print("\n=== 测试落子操作 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 玩家1在中心位置落子
    board.put_chess(4, 1)
    
    # 验证状态变化
    assert board.state_pos & board.mask_sets[4], "位置4应该有棋子"
    assert board.state_statu & board.mask_sets[4], "位置4应该是玩家1"
    
    # 玩家2落子
    board.put_chess(1, 2)
    assert board.state_pos & board.mask_sets[1], "位置1应该有棋子"
    assert not (board.state_statu & board.mask_sets[1]), "位置1应该是玩家2"
    
    # 玩家1再次落子
    board.put_chess(2, 1)
    assert board.state_pos & board.mask_sets[2], "位置2应该有棋子"
    assert board.state_statu & board.mask_sets[2], "位置2应该是玩家1"
    
    print("✅ 落子操作测试通过")


def test_remove_chess():
    """测试移除棋子"""
    print("\n=== 测试移除棋子 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 放置棋子
    board.put_chess(4, 1)
    assert board.state_pos & board.mask_sets[4], "位置4应该有棋子"
    
    # 移除棋子
    board.put_chess(4, 0)
    assert not (board.state_pos & board.mask_sets[4]), "位置4应该没有棋子"
    assert not (board.state_statu & board.mask_sets[4]), "位置4应该没有状态"
    
    print("✅ 移除棋子测试通过")


def test_state_management():
    """测试状态管理"""
    print("\n=== 测试状态管理 ===")
    
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
    
    # 验证状态一致性
    assert board.state_pos == board2.state_pos, f"state_pos 不一致: {board.state_pos} vs {board2.state_pos}"
    assert board.state_statu == board2.state_statu, f"state_statu 不一致: {board.state_statu} vs {board2.state_statu}"
    
    print("✅ 状态管理测试通过")


def test_string_state_conversion():
    """测试字符串状态转换"""
    print("\n=== 测试字符串状态转换 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 通过字符串设置状态
    board.change_grid("0|1|2|3|4|5")
    
    # 验证落子顺序和玩家
    for i in range(6):
        assert board.state_pos & board.mask_sets[i], f"位置{i}应该有棋子"
        # 验证玩家交替
        expected_player = (i % 2) + 1
        if expected_player == 1:
            assert board.state_statu & board.mask_sets[i], f"位置{i}应该是玩家1"
        else:
            assert not (board.state_statu & board.mask_sets[i]), f"位置{i}应该是玩家2"
    
    print("✅ 字符串状态转换测试通过")


def test_format_output():
    """测试格式化输出"""
    print("\n=== 测试格式化输出 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 测试空棋盘
    board_str = board.to_str({})
    assert len(board_str) == 4, f"棋盘应该有4行，实际有{len(board_str)}行"
    assert "0 1 2" in board_str[3], "坐标行应该包含 '0 1 2'"
    
    # 放置一些棋子
    board.put_chess(0, 1)  # 玩家1 -> 'O'
    board.put_chess(1, 2)  # 玩家2 -> 'X'
    board.put_chess(3, 1)  # 玩家1 -> 'O'
    
    board_str = board.to_str({})
    board_str_combined = "\n".join(board_str)
    
    assert "O" in board_str_combined, "棋盘应该包含 'O'"
    assert "X" in board_str_combined, "棋盘应该包含 'X'"
    
    print("✅ 格式化输出测试通过")


def test_format_function():
    """测试 format 函数"""
    print("\n=== 测试 format 函数 ===")
    
    from app.yly.envs.game.c5.board.base import format
    
    assert format(0) == "-", "空位置应该显示为 '-'"
    assert format(1) == "O", "玩家1应该显示为 'O'"
    assert format(2) == "X", "玩家2应该显示为 'X'"
    
    # 测试边界值
    assert format(-1) == "-", "负数应该显示为 '-'"
    assert format(3) == "-", "超出范围应该显示为 '-'"
    
    print("✅ format 函数测试通过")


def test_constants():
    """测试常量"""
    print("\n=== 测试常量 ===")
    
    board = BoardC5()
    
    # 验证状态常量
    assert board.STATE_NULL == 0, "STATE_NULL 应该是 0"
    assert board.STATE_FIRST == 1, "STATE_FIRST 应该是 1"
    assert board.STATE_SECONED == 2, "STATE_SECONED 应该是 2"
    
    # 验证方向常量
    expected_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    assert board.DR == expected_directions, f"方向常量不正确: {board.DR}"
    
    print("✅ 常量测试通过")


def test_load_records():
    """测试通过记录加载"""
    print("\n=== 测试通过记录加载 ===")
    
    board = BoardC5().load(3, 3, 3)
    
    # 通过记录加载
    records = [0, 1, 2, 3, 4, 5]
    board.load_records(records)
    
    # 验证所有位置都有棋子
    for i in range(6):
        assert board.state_pos & board.mask_sets[i], f"位置{i}应该有棋子"
        # 验证玩家交替
        expected_player = (i % 2) + 1
        if expected_player == 1:
            assert board.state_statu & board.mask_sets[i], f"位置{i}应该是玩家1"
        else:
            assert not (board.state_statu & board.mask_sets[i]), f"位置{i}应该是玩家2"
    
    print("✅ 通过记录加载测试通过")


def main():
    """主函数"""
    print("开始运行 BoardC5 测试...")
    
    try:
        test_basic_initialization()
        test_minimal_board()
        test_put_chess()
        test_remove_chess()
        test_state_management()
        test_string_state_conversion()
        test_format_output()
        test_format_function()
        test_constants()
        test_load_records()
        
        print("\n🎉 所有测试通过!")
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())