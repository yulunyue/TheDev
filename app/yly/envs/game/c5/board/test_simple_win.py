#!/usr/bin/env python3
"""
简单的胜负检测测试
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
for i in range(6):
    project_root = os.path.dirname(project_root)

sys.path.insert(0, project_root)

from app.yly.envs.game.c5.board.base import BoardC5

# 创建棋盘
board = BoardC5().load(5, 5, 3)

# 创建横向三连珠（玩家1）
print("创建横向三连珠（玩家1）")
board.put_chess(0, 1)  # 玩家1在(0,0)
board.put_chess(1, 1)  # 玩家1在(0,1)
board.put_chess(2, 1)  # 玩家1在(0,2)

# 显示棋盘
print("棋盘状态:")
for line in board.to_str({}):
    print(line)

# 检查获胜
print("\n检查获胜情况:")
for idx in range(3):
    y = idx // 5
    x = idx % 5
    is_win = board.check_win(idx, 1)
    print(f"位置{idx} 坐标({y}, {x}): 玩家1, 获胜: {is_win}")

# 测试玩家2获胜
print("\n=== 测试玩家2获胜 ===")
board2 = BoardC5().load(5, 5, 3)
board2.put_chess(5, 2)  # 玩家2在(1,0)
board2.put_chess(6, 2)  # 玩家2在(1,1)
board2.put_chess(7, 2)  # 玩家2在(1,2)

print("棋盘状态:")
for line in board2.to_str({}):
    print(line)

print("检查获胜情况:")
for idx in range(5, 8):
    y = idx // 5
    x = idx % 5
    is_win = board2.check_win(idx, 2)
    print(f"位置{idx} 坐标({y}, {x}): 玩家2, 获胜: {is_win}")

# 测试纵向获胜
print("\n=== 测试纵向获胜 ===")
board3 = BoardC5().load(5, 5, 3)
board3.put_chess(0, 1)  # 玩家1在(0,0)
board3.put_chess(5, 1)  # 玩家1在(1,0)
board3.put_chess(10, 1)  # 玩家1在(2,0)

print("棋盘状态:")
for line in board3.to_str({}):
    print(line)

print("检查获胜情况:")
for idx in [0, 5, 10]:
    y = idx // 5
    x = idx % 5
    is_win = board3.check_win(idx, 1)
    print(f"位置{idx} 坐标({y}, {x}): 玩家1, 获胜: {is_win}")