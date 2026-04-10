#!/usr/bin/env python3
"""
C5 Models 测试用例

测试 ChessState、ChessAction、ChessStateMap 和数据库配置
"""

import sys
import os
import tempfile
import json

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
for i in range(6):
    project_root = os.path.dirname(project_root)

sys.path.insert(0, project_root)

from app.yly.envs.game.c5.model.chess_state import CState664
from app.yly.envs.game.c5.model.chess_action import ChessACtion
from app.yly.envs.game.c5.model.chess_state_map import CState333, CHESS_MAP_CLS_FUNC
from app.yly.envs/game/c5/model.db import Bd


class TestChessState:
    """测试 ChessState 类"""
    
    def test_cstate664_creation(self):
        """测试 CState664 创建"""
        print("=== 测试 CState664 创建 ===")
        
        # 创建初始状态
        state = CState664.set_board()
        
        # 验证属性
        assert state.w == 6, f"宽度应该是6，实际是{state.w}"
        assert state.h == 6, f"高度应该是6，实际是{state.h}"
        assert state.in_row == 4, f"获胜条件应该是4，实际是{state.in_row}"
        assert state.env is not None, "环境应该被设置"
        assert state.state == 0, f"初始状态应该是0，实际是{state.state}"
        assert state.depth == 0, f"初始深度应该是0，实际是{state.depth}"
        assert state.player_id == 0, f"初始玩家应该是0，实际是{state.player_id}"
        
        print("✅ CState664 创建测试通过")
    
    def test_cstate333_creation(self):
        """测试 CState333 创建"""
        print("\n=== 测试 CState333 创建 ===")
        
        # 创建初始状态
        state = CState333.set_board()
        
        # 验证属性
        assert state.w == 3, f"宽度应该是3，实际是{state.w}"
        assert state.h == 3, f"高度应该是3，实际是{state.h}"
        assert state.in_row == 3, f"获胜条件应该是3，实际是{state.in_row}"
        
        print("✅ CState333 创建测试通过")
    
    def test_state_from_string(self):
        """测试从字符串创建状态"""
        print("\n=== 测试从字符串创建状态 ===")
        
        # 使用字符串状态
        string_state = "0|1|2|3|4|5"
        state = CState664.set_board(string_state)
        
        # 验证状态
        assert state.state != 0, "状态应该被设置"
        assert state.depth == 6, f"深度应该是6，实际是{state.depth}"
        assert state.player_id == 0, f"玩家ID应该是0，实际是{state.player_id}"
        
        print("✅ 从字符串创建状态测试通过")
    
    def test_action_generation(self):
        """测试动作生成"""
        print("\n=== 测试动作生成 ===")
        
        # 创建状态
        state = CState664.set_board()
        
        # 生成动作
        actions = state.make_actions()
        
        # 验证动作
        assert len(actions) > 0, "应该有动作"
        assert len(actions) == 36, f"6x6棋盘应该有36个动作，实际是{len(actions)}"
        
        # 验证第一个动作
        first_action = actions[0]
        assert isinstance(first_action, ChessACtion), "动作应该是 ChessACtion 实例"
        assert first_action.src == state, "源状态应该是当前状态"
        assert first_action.action >= 0, "动作应该是有效的位置"
        assert first_action.dst is not None, "目标状态应该被设置"
        
        print("✅ 动作生成测试通过")
    
    def test_state_transition(self):
        """测试状态转换"""
        print("\n=== 测试状态转换 ===")
        
        # 创建状态
        state = CState664.set_board()
        
        # 执行动作
        action = state.get_action(10)  # 位置10
        new_state = action.dst
        
        # 验证转换
        assert new_state != state, "新状态应该与原状态不同"
        assert new_state.depth == state.depth + 1, f"深度应该增加1，实际是{new_state.depth - state.depth}"
        assert new_state.player_id == 1 - state.player_id, f"玩家应该切换，原玩家{state.player_id}，新玩家{new_state.player_id}"
        
        print("✅ 状态转换测试通过")


class TestChessAction:
    """测试 ChessAction 类"""
    
    def test_action_creation(self):
        """测试动作创建"""
        print("\n=== 测试动作创建 ===")
        
        # 创建状态
        src_state = CState664.set_board()
        
        # 创建动作
        action = src_state.get_action(10)
        
        # 验证动作
        assert action.src == src_state, "源状态应该正确"
        assert action.action == 10, "动作应该是10"
        assert action.dst is not None, "目标状态应该存在"
        assert action.obs is not None, "观察信息应该存在"
        assert isinstance(action.reward, (int, float)), "奖励应该是数字"
        
        print("✅ 动作创建测试通过")
    
    def test_action_reward_calculation(self):
        """测试动作奖励计算"""
        print("\n=== 测试动作奖励计算 ===")
        
        # 创建状态
        src_state = CState664.set_board()
        
        # 创建动作
        action = src_state.get_action(10)
        
        # 模拟获胜观察
        win_obs = {(src_state.env.in_row, 0): True}
        action.set_obs(win_obs)
        
        # 验证奖励
        assert action.reward == 1, "获胜奖励应该是1"
        assert action.dst.done == src_state.player_id + 1, "目标状态应该标记为完成"
        
        print("✅ 动作奖励计算测试通过")


class TestChessStateMap:
    """测试 ChessStateMap 类"""
    
    def test_class_mapping(self):
        """测试类映射"""
        print("\n=== 测试类映射 ===")
        
        # 验证映射包含
        assert "CState664" in CHESS_MAP_CLS_FUNC, "映射应该包含 CState664"
        assert "CState333" in CHESS_MAP_CLS_FUNC, "映射应该包含 CState333"
        
        # 验证类实例
        cstate664_cls = CHESS_MAP_CLS_FUNC["CState664"]
        assert cstate664_cls == CState664, "映射应该返回正确的类"
        
        cstate333_cls = CHESS_MAP_CLS_FUNC["CState333"]
        assert cstate333_cls == CState333, "映射应该返回正确的类"
        
        print("✅ 类映射测试通过")
    
    def test_inheritance(self):
        """测试继承关系"""
        print("\n=== 测试继承关系 ===")
        
        # 验证继承
        assert issubclass(CState333, CState664), "CState333 应该继承 CState664"
        
        # 验证属性覆盖
        assert CState333.w == 3, "CState333 应该覆盖宽度"
        assert CState333.h == 3, "CState333 应该覆盖高度"
        assert CState333.in_row == 3, "CState333 应该覆盖获胜条件"
        
        print("✅ 继承关系测试通过")


def main():
    """主函数"""
    print("开始运行 C5 Models 测试...")
    
    try:
        # 创建测试实例
        test_state = TestChessState()
        test_action = TestChessAction()
        test_state_map = TestChessStateMap()
        
        # 运行测试
        test_state.test_cstate664_creation()
        test_state.test_cstate333_creation()
        test_state.test_state_from_string()
        test_state.test_action_generation()
        test_state.test_state_transition()
        
        test_action.test_action_creation()
        test_action.test_action_reward_calculation()
        
        test_state_map.test_class_mapping()
        test_state_map.test_inheritance()
        
        print("\n🎉 所有 C5 Models 测试通过!")
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())