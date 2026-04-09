#!/usr/bin/env python3
"""
调试状态位逻辑
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
board = BoardC5().load(3, 3, 3)

# 放置棋子
print("=== 放置棋子并检查状态 ===")

# 玩家1落子
print("玩家1在位置0落子:")
board.put_chess(0, 1)
print(f"  state_pos: {bin(board.state_pos)}")
print(f"  state_statu: {bin(board.state_statu)}")
print(f"  位置0有棋子: {board.state_pos & board.mask_sets[0]}")
print(f"  位置0是玩家1: {board.state_statu & board.mask_sets[0]}")

# 玩家2落子
print("\n玩家2在位置1落子:")
board.put_chess(1, 2)
print(f"  state_pos: {bin(board.state_pos)}")
print(f"  state_statu: {bin(board.state_statu)}")
print(f"  位置1有棋子: {board.state_pos & board.mask_sets[1]}")
print(f"  位置1是玩家1: {board.state_statu & board.mask_sets[1]}")
print(f"  位置1是玩家2: {not (board.state_statu & board.mask_sets[1])}")

# 玩家1落子
print("\n玩家1在位置2落子:")
board.put_chess(2, 1)
print(f"  state_pos: {bin(board.state_pos)}")
print(f"  state_statu: {bin(board.state_statu)}")
print(f"  位置2有棋子: {board.state_pos & board.mask_sets[2]}")
print(f"  位置2是玩家1: {board.state_statu & board.mask_sets[2]}")

# 测试获胜检测
print("\n=== 测试获胜检测 ===")
print("检查位置0:")
idx = 0
y = idx // 3
x = idx % 3
print(f"坐标: ({y}, {x})")
print(f"玩家1: {board.check_win(idx, 1)}")
print(f"玩家2: {board.check_win(idx, 2)}")

print("\n检查位置1:")
idx = 1
y = idx // 3
x = idx % 3
print(f"坐标: ({y}, {x})")
print(f"玩家1: {board.check_win(idx, 1)}")
print(f"玩家2: {board.check_win(idx, 2)}")

print("\n检查位置2:")
idx = 2
y = idx // 3
x = idx % 3
print(f"坐标: ({y}, {x})")
print(f"玩家1: {board.check_win(idx, 1)}")
print(f"玩家2: {board.check_win(idx, 2)}")

# 显示棋盘
print("\n=== 棋盘显示 ===")
for line in board.to_str({}):
    print(line)