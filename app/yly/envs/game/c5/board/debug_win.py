#!/usr/bin/env python3
"""
调试胜负检测功能
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

# 放置棋子
moves = [0, 1, 1, 2, 2, 3, 3, 4, 4]
for i, move in enumerate(moves):
    board.put_chess(move, (i % 2) + 1)
    print(f"玩家{(i % 2) + 1}在位置{move}落子")

# 显示棋盘
print("\n棋盘状态:")
for line in board.to_str({}):
    print(line)

# 检查每个位置的获胜情况
print("\n检查每个位置的获胜情况:")
for idx in range(25):
    if board.state_pos & board.mask_sets[idx]:
        player = 1 if board.state_statu & board.mask_sets[idx] else 2
        is_win = board.check_win(idx, player)
        print(f"位置{idx}: 玩家{player}, 获胜: {is_win}")

# 检查游戏状态
winner = board.get_winner()
is_over = board.is_game_over()
print(f"\n获胜者: {winner}")
print(f"游戏结束: {is_over}")

# 检查特定位置
print(f"\n检查位置4的详细信息:")
idx = 4
y = idx // 5
x = idx % 5
print(f"坐标: ({y}, {x})")
print(f"位置有棋子: {board.state_pos & board.mask_sets[idx]}")
print(f"玩家: {1 if board.state_statu & board.mask_sets[idx] else 2}")

# 检查四个方向
print(f"\n检查四个方向:")
for dy, dx in board.DR:
    result = board._check_line_win(y, x, dy, dx, 1)
    print(f"方向({dy}, {dx}): {result}")