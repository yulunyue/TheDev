#!/usr/bin/env python3
"""
调试棋盘坐标系统
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

# 测试坐标转换
print("=== 坐标转换测试 ===")
for idx in range(25):
    y = idx // 5
    x = idx % 5
    print(f"位置{idx} -> 坐标({y}, {x})")

# 放置横向棋子
print("\n=== 放置横向棋子 ===")
horizontal_moves = [0, 1, 2, 3, 4]  # 横向第一行
for i, idx in enumerate(horizontal_moves):
    player = (i % 2) + 1
    board.put_chess(idx, player)
    y = idx // 5
    x = idx % 5
    print(f"玩家{player}在位置{idx}落子 -> 坐标({y}, {x})")

# 显示棋盘
print("\n棋盘状态:")
for line in board.to_str({}):
    print(line)

# 检查获胜情况
print("\n检查获胜情况:")
for idx in range(25):
    if board.state_pos & board.mask_sets[idx]:
        player = 1 if board.state_statu & board.mask_sets[idx] else 2
        is_win = board.check_win(idx, player)
        y = idx // 5
        x = idx % 5
        print(f"位置{idx} 坐标({y}, {x}): 玩家{player}, 获胜: {is_win}")

# 检查最后一个棋子
print(f"\n检查最后一个棋子(位置4):")
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
    
    # 详细检查这个方向
    print(f"  详细检查方向({dy}, {dx}):")
    if dy == 0 and dx == 1:  # 横向
        for i in range(5):
            check_idx = y * 5 + (x + i)
            if 0 <= check_idx < 25:
                has_piece = board.state_pos & board.mask_sets[check_idx]
                player = "无" if not has_piece else ("1" if board.state_statu & board.mask_sets[check_idx] else "2")
                print(f"    位置{check_idx} 坐标({y}, {x + i}): 有棋子={has_piece}, 玩家={player}")