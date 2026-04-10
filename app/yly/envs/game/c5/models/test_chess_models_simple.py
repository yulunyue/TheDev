#!/usr/bin/env python3
"""
C5 Models 简单测试用例

测试 ChessState、ChessAction、ChessStateMap 的基本功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
for i in range(6):
    project_root = os.path.dirname(project_root)

sys.path.insert(0, project_root)

def test_basic_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    
    try:
        from app.yly.envs.game.c5.model.chess_state import CState664
        print("✅ CState664 导入成功")
        
        from app.yly.envs.game.c5.model.chess_action import ChessACtion
        print("✅ ChessACtion 导入成功")
        
        from app.yly.envs.game.c5.model.chess_state_map import CState333, CHESS_MAP_CLS_FUNC
        print("✅ CState333 和 CHESS_MAP_CLS_FUNC 导入成功")
        
        from app.yly.envs.game.c5.model.db import Bd
        print("✅ Bd 导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_cstate_creation():
    """测试 CState 创建"""
    print("\n=== 测试 CState 创建 ===")
    
    try:
        from app.yly.envs.game.c5.model.chess_state import CState664, CState333
        
        # 测试 CState664
        state664 = CState664.set_board()
        assert state664.w == 6, f"宽度应该是6，实际是{state664.w}"
        assert state664.h == 6, f"高度应该是6，实际是{state664.h}"
        assert state664.in_row == 4, f"获胜条件应该是4，实际是{state664.in_row}"
        print("✅ CState664 创建成功")
        
        # 测试 CState333
        state333 = CState333.set_board()
        assert state333.w == 3, f"宽度应该是3，实际是{state333.w}"
        assert state333.h == 3, f"高度应该是3，实际是{state333.h}"
        assert state333.in_row == 3, f"获胜条件应该是3，实际是{state333.in_row}"
        print("✅ CState333 创建成功")
        
        return True
    except Exception as e:
        print(f"❌ CState 创建失败: {e}")
        return False


def test_action_creation():
    """测试动作创建"""
    print("\n=== 测试动作创建 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state import CState664
        from app.yly/envs/game/c5.model.chess_action import ChessACtion
        
        # 创建状态
        state = CState664.set_board()
        
        # 创建动作
        action = state.get_action(10)
        
        # 验证动作
        assert action.src == state, "源状态应该正确"
        assert action.action == 10, "动作应该是10"
        assert action.dst is not None, "目标状态应该存在"
        assert action.obs is not None, "观察信息应该存在"
        assert isinstance(action.reward, (int, float)), "奖励应该是数字"
        print("✅ 动作创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 动作创建失败: {e}")
        return False


def test_state_transition():
    """测试状态转换"""
    print("\n=== 测试状态转换 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state import CState664
        
        # 创建状态
        state = CState664.set_board()
        
        # 执行动作
        action = state.get_action(10)  # 位置10
        new_state = action.dst
        
        # 验证转换
        assert new_state != state, "新状态应该与原状态不同"
        assert new_state.depth == state.depth + 1, f"深度应该增加1，实际是{new_state.depth - state.depth}"
        assert new_state.player_id == 1 - state.player_id, f"玩家应该切换，原玩家{state.player_id}，新玩家{new_state.player_id}"
        print("✅ 状态转换成功")
        
        return True
    except Exception as e:
        print(f"❌ 状态转换失败: {e}")
        return False


def test_action_reward():
    """测试动作奖励"""
    print("\n=== 测试动作奖励 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state import CState664
        from app.yly/envs/game/c5.model.chess_action import ChessACtion
        
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
        print("✅ 动作奖励计算成功")
        
        return True
    except Exception as e:
        print(f"❌ 动作奖励计算失败: {e}")
        return False


def test_class_mapping():
    """测试类映射"""
    print("\n=== 测试类映射 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state_map import CState664, CState333, CHESS_MAP_CLS_FUNC
        
        # 验证映射包含
        assert "CState664" in CHESS_MAP_CLS_FUNC, "映射应该包含 CState664"
        assert "CState333" in CHESS_MAP_CLS_FUNC, "映射应该包含 CState333"
        
        # 验证类实例
        cstate664_cls = CHESS_MAP_CLS_FUNC["CState664"]
        assert cstate664_cls == CState664, "映射应该返回正确的类"
        
        cstate333_cls = CHESS_MAP_CLS_FUNC["CState333"]
        assert cstate333_cls == CState333, "映射应该返回正确的类"
        print("✅ 类映射测试成功")
        
        return True
    except Exception as e:
        print(f"❌ 类映射测试失败: {e}")
        return False


def test_inheritance():
    """测试继承关系"""
    print("\n=== 测试继承关系 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state_map import CState664, CState333
        
        # 验证继承
        assert issubclass(CState333, CState664), "CState333 应该继承 CState664"
        
        # 验证属性覆盖
        assert CState333.w == 3, "CState333 应该覆盖宽度"
        assert CState333.h == 3, "CState333 应该覆盖高度"
        assert CState333.in_row == 3, "CState333 应该覆盖获胜条件"
        print("✅ 继承关系测试成功")
        
        return True
    except Exception as e:
        print(f"❌ 继承关系测试失败: {e}")
        return False


def test_bd_creation():
    """测试 Bd 创建"""
    print("\n=== 测试 Bd 创建 ===")
    
    try:
        from app.yly.envs/game/c5.model.db import Bd
        
        # 创建配置
        bd = Bd()
        
        # 验证属性
        assert bd.name is not None, "名称应该被设置"
        assert bd.size is not None, "尺寸应该被设置"
        assert bd.records is not None, "记录应该被设置"
        assert bd.p0 is not None, "玩家0应该被设置"
        assert bd.p1 is not None, "玩家1应该被设置"
        print("✅ Bd 创建成功")
        
        return True
    except Exception as e:
        print(f"❌ Bd 创建失败: {e}")
        return False


def test_string_state():
    """测试字符串状态"""
    print("\n=== 测试字符串状态 ===")
    
    try:
        from app.yly.envs/game/c5.model.chess_state import CState664
        
        # 使用字符串状态
        string_state = "0|1|2|3|4|5"
        state = CState664.set_board(string_state)
        
        # 验证状态
        assert state.state != 0, "状态应该被设置"
        assert state.depth == 6, f"深度应该是6，实际是{state.depth}"
        assert state.player_id == 0, f"玩家ID应该是0，实际是{state.player_id}"
        print("✅ 字符串状态测试成功")
        
        return True
    except Exception as e:
        print(f"❌ 字符串状态测试失败: {e}")
        return False


def main():
    """主函数"""
    print("开始运行 C5 Models 简单测试...")
    
    tests = [
        test_basic_imports,
        test_cstate_creation,
        test_action_creation,
        test_state_transition,
        test_action_reward,
        test_class_mapping,
        test_inheritance,
        test_bd_creation,
        test_string_state,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有 C5 Models 简单测试通过!")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1


if __name__ == '__main__':
    exit(main())