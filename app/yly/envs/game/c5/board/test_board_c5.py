"""
BoardC5 测试用例

测试 BoardC5 类的所有功能，包括：
- 初始化和配置
- 落子操作
- 状态管理
- 格式化输出
- 边界条件
- 性能测试
"""

import unittest
import sys
import os
import time
from typing import List, Dict, Any

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
sys.path.insert(0, project_root)

from app.yly.envs.game.c5.board.base import BoardC5


class TestBoardC5Initialization(unittest.TestCase):
    """测试 BoardC5 初始化功能"""
    
    def test_basic_initialization(self):
        """测试基本棋盘初始化"""
        board = BoardC5()
        result = board.load(15, 15, 5)
        
        # 验证返回对象
        self.assertEqual(result, board)
        
        # 验证属性设置
        self.assertEqual(board.width, 15)
        self.assertEqual(board.height, 15)
        self.assertEqual(board.in_row, 5)
        self.assertEqual(board.size, 225)
        
        # 验证掩码设置
        self.assertEqual(board.mask_h, (1 << 15) - 1)
        self.assertEqual(board.mask_full, (1 << 225) - 1)
        
        # 验证初始状态
        self.assertEqual(board.state_pos, 0)
        self.assertEqual(board.state_statu, 0)
    
    def test_minimal_board(self):
        """测试最小棋盘（3x3, 3子连线）"""
        board = BoardC5()
        board.load(3, 3, 3)
        
        self.assertEqual(board.width, 3)
        self.assertEqual(board.height, 3)
        self.assertEqual(board.in_row, 3)
        self.assertEqual(board.size, 9)
        self.assertEqual(board.mask_h, (1 << 3) - 1)
        self.assertEqual(board.mask_full, (1 << 9) - 1)
    
    def test_large_board(self):
        """测试大棋盘（20x20, 5子连线）"""
        board = BoardC5()
        board.load(20, 20, 5)
        
        self.assertEqual(board.width, 20)
        self.assertEqual(board.height, 20)
        self.assertEqual(board.in_row, 5)
        self.assertEqual(board.size, 400)
        self.assertEqual(board.mask_h, (1 << 20) - 1)
        self.assertEqual(board.mask_full, (1 << 400) - 1)
    
    def test_board_directions(self):
        """测试棋盘方向常量"""
        board = BoardC5()
        board.load(15, 15, 5)
        
        # 验证方向常量
        expected_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
        self.assertEqual(board.DR, expected_directions)
    
    def test_state_constants(self):
        """测试状态常量"""
        board = BoardC5()
        
        # 验证状态常量
        self.assertEqual(board.STATE_NULL, 0)
        self.assertEqual(board.STATE_FIRST, 1)
        self.assertEqual(board.STATE_SECONED, 2)


class TestBoardC5PutChess(unittest.TestCase):
    """测试 BoardC5 落子操作"""
    
    def setUp(self):
        """测试前准备"""
        self.board = BoardC5().load(3, 3, 3)
    
    def test_basic_put_chess(self):
        """测试基本落子操作"""
        # 玩家1在中心位置落子
        self.board.put_chess(4, 1)  # 中心位置索引
        
        # 验证状态变化
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[4])
        
        # 验证棋盘显示
        board_str = self.board.to_str({})
        board_str_combined = "\n".join(board_str)
        self.assertIn("O", board_str_combined)  # 玩家1显示为'O'
    
    def test_put_chess_player2(self):
        """测试玩家2落子"""
        # 玩家2落子
        self.board.put_chess(4, 2)
        
        # 验证状态变化
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[4])  # 玩家2
        
        # 验证棋盘显示
        board_str = self.board.to_str({})
        board_str_combined = "\n".join(board_str)
        self.assertIn("X", board_str_combined)  # 玩家2显示为'X'
    
    def test_alternate_players(self):
        """测试玩家交替落子"""
        # 玩家1落子
        self.board.put_chess(0, 1)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[0])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[0])  # 玩家1
        
        # 玩家2落子
        self.board.put_chess(1, 2)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[1])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[1])  # 玩家2
        
        # 玩家1再次落子
        self.board.put_chess(2, 1)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[2])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[2])  # 玩家1
    
    def test_remove_chess(self):
        """测试移除棋子"""
        # 放置棋子
        self.board.put_chess(4, 1)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        
        # 移除棋子
        self.board.put_chess(4, 0)
        self.assertFalse(self.board.state_pos & self.board.mask_sets[4])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[4])
    
    def test_put_chess_same_position(self):
        """测试同一位置重复落子"""
        # 玩家1落子
        self.board.put_chess(4, 1)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[4])
        
        # 玩家2在同一位置落子
        self.board.put_chess(4, 2)
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[4])
        
        # 移除棋子
        self.board.put_chess(4, 0)
        self.assertFalse(self.board.state_pos & self.board.mask_sets[4])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[4])


class TestBoardC5StateManagement(unittest.TestCase):
    """测试 BoardC5 状态管理"""
    
    def setUp(self):
        """测试前准备"""
        self.board = BoardC5().load(3, 3, 3)
    
    def test_state_set_get(self):
        """测试状态设置和获取"""
        # 设置一些棋子
        self.board.put_chess(0, 1)
        self.board.put_chess(1, 2)
        self.board.put_chess(2, 1)
        
        # 获取状态
        state = self.board.get_state()
        
        # 创建新棋盘并设置状态
        board2 = BoardC5().load(3, 3, 3)
        board2.set_state(state)
        
        # 验证状态一致性
        self.assertEqual(self.board.state_pos, board2.state_pos)
        self.assertEqual(self.board.state_statu, board2.state_statu)
    
    def test_string_state_conversion(self):
        """测试字符串状态转换"""
        # 通过字符串设置状态
        self.board.change_grid("0|1|2|3|4|5")
        
        # 验证落子顺序和玩家
        # 位置0: 玩家1, 位置1: 玩家2, 位置2: 玩家1, 位置3: 玩家2, 位置4: 玩家1, 位置5: 玩家2
        self.assertTrue(self.board.state_pos & self.board.mask_sets[0])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[0])  # 玩家1
        
        self.assertTrue(self.board.state_pos & self.board.mask_sets[1])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[1])  # 玩家2
        
        self.assertTrue(self.board.state_pos & self.board.mask_sets[2])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[2])  # 玩家1
        
        self.assertTrue(self.board.state_pos & self.board.mask_sets[3])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[3])  # 玩家2
        
        self.assertTrue(self.board.state_pos & self.board.mask_sets[4])
        self.assertTrue(self.board.state_statu & self.board.mask_sets[4])  # 玩家1
        
        self.assertTrue(self.board.state_pos & self.board.mask_sets[5])
        self.assertFalse(self.board.state_statu & self.board.mask_sets[5])  # 玩家2
    
    def test_load_records(self):
        """测试通过记录加载"""
        # 通过记录加载
        records = [0, 1, 2, 3, 4, 5]
        self.board.load_records(records)
        
        # 验证所有位置都有棋子
        for i in range(6):
            self.assertTrue(self.board.state_pos & self.board.mask_sets[i])
            # 验证玩家交替
            expected_player = (i % 2) + 1
            if expected_player == 1:
                self.assertTrue(self.board.state_statu & self.board.mask_sets[i])
            else:
                self.assertFalse(self.board.state_statu & self.board.mask_sets[i])


class TestBoardC5FormatOutput(unittest.TestCase):
    """测试 BoardC5 格式化输出"""
    
    def setUp(self):
        """测试前准备"""
        self.board = BoardC5().load(3, 3, 3)
    
    def test_empty_board_format(self):
        """测试空棋盘格式化"""
        board_str = self.board.to_str({})
        
        # 验证棋盘结构
        self.assertEqual(len(board_str), 4)  # 3行棋盘 + 1行坐标
        
        # 验证坐标显示
        self.assertIn("0 1 2", board_str[3])
        
        # 验证空位置显示
        for i in range(3):
            self.assertIn(" ", board_str[i])
    
    def test_board_with_pieces_format(self):
        """测试有棋子棋盘格式化"""
        # 放置一些棋子
        self.board.put_chess(0, 1)  # 玩家1 -> 'O'
        self.board.put_chess(1, 2)  # 玩家2 -> 'X'
        self.board.put_chess(3, 1)  # 玩家1 -> 'O'
        
        board_str = self.board.to_str({})
        
        # 验证棋子显示
        board_str_combined = "\n".join(board_str)
        self.assertIn("O", board_str_combined)  # 位置0
        self.assertIn("X", board_str_combined)  # 位置1
        self.assertIn("O", board_str_combined)  # 位置3
    
    def test_format_function(self):
        """测试 format 函数"""
        from app.yly.envs.game.c5.board.base import format
        
        self.assertEqual(format(0), "-")  # 空位置
        self.assertEqual(format(1), "O")  # 玩家1
        self.assertEqual(format(2), "X")  # 玩家2
        
        # 测试边界值
        self.assertEqual(format(-1), "-")
        self.assertEqual(format(3), "-")


class TestBoardC5Simple(unittest.TestCase):
    """简化的 BoardC5 测试"""
    
    def test_basic_functionality(self):
        """测试基本功能"""
        # 创建棋盘
        board = BoardC5()
        board.load(3, 3, 3)
        
        # 放置棋子
        board.put_chess(0, 1)  # 玩家1
        board.put_chess(1, 2)  # 玩家2
        board.put_chess(2, 1)  # 玩家1
        
        # 验证状态
        self.assertTrue(board.state_pos & board.mask_sets[0])
        self.assertTrue(board.state_pos & board.mask_sets[1])
        self.assertTrue(board.state_pos & board.mask_sets[2])
        
        # 验证玩家
        self.assertTrue(board.state_statu & board.mask_sets[0])  # 玩家1
        self.assertFalse(board.state_statu & board.mask_sets[1])  # 玩家2
        self.assertTrue(board.state_statu & board.mask_sets[2])  # 玩家1
        
        # 验证格式化输出
        board_str = board.to_str({})
        self.assertIsInstance(board_str, list)
        self.assertEqual(len(board_str), 4)
        
        # 验证字符串包含棋子
        board_str_combined = "\n".join(board_str)
        self.assertIn("O", board_str_combined)
        self.assertIn("X", board_str_combined)


def run_all_tests():
    """运行所有测试"""
    print("开始运行 BoardC5 测试...")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestBoardC5Initialization,
        TestBoardC5PutChess,
        TestBoardC5StateManagement,
        TestBoardC5FormatOutput,
        TestBoardC5Simple,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print(f"\n测试总结:")
    print(f"  总计: {result.testsRun}")
    print(f"  通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败: {len(result.failures)}")
    print(f"  错误: {len(result.errors)}")
    
    if result.failures:
        print(f"\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)