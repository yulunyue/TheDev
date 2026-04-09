#!/usr/bin/env python3
"""
调试平局检测
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

# 填满棋盘
print("=== 填满棋盘 ===")
for i in range(9):
    player = (i % 2) + 1
    board.put_chess(i, player)
    print(f"玩家{player}在位置{i}落子")

# 显示棋盘
print("\n棋盘状态:")
for line in board.to_str({}):
    print(line)

# 检查状态
print("\n=== 检查状态 ===")
print(f"state_pos: {bin(board.state_pos)}")
print(f"state_statu: {bin(board.state_statu)}")
print(f"mask_full: {bin(board.mask_full)}")
print(f"state_pos == mask_full: {board.state_pos == board.mask_full}")

# 检查每个位置
print("\n=== 检查每个位置 ===")
for i in range(9):
    has_piece = board.state_pos & board.mask_sets[i]
    player = 1 if board.state_statu & board.mask_sets[i] else 2
    print(f"位置{i}: 有棋子={has_piece}, 玩家={player}")

# 检查获胜情况
print("\n=== 检查获胜情况 ===")
winner = board.get_winner()
is_over = board.is_game_over()
print(f"获胜者: {winner}")
print(f"游戏结束: {is_over}")

# 检查是否有获胜者
print("\n=== 检查是否有获胜者 ===")
for idx in range(9):
    if board.state_pos & board.mask_sets[idx]:
        player = 1 if board.state_statu & board.mask_sets[idx] else 2
        is_win = board.check_win(idx, player)
        print(f"位置{idx}: 玩家{player}, 获胜: {is_win}")