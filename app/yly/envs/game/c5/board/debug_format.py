#!/usr/bin/env python3
"""
调试棋盘格式化
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

# 放置一些棋子
board.put_chess(0, 1)  # 玩家1 -> 'O'
board.put_chess(1, 2)  # 玩家2 -> 'X'
board.put_chess(4, 1)  # 玩家1 -> 'O'

# 获取格式化输出
board_str = board.to_str({})
print("棋盘字符串:")
for i, line in enumerate(board_str):
    print(f"行{i}: {line}")

print(f"\n合并后的字符串:")
board_str_combined = "\n".join(board_str)
print(board_str_combined)

print(f"\n检查字符:")
print(f"包含 'O': {'O' in board_str_combined}")
print(f"包含 'X': {'X' in board_str_combined}")
print(f"包含 '-': {'-' in board_str_combined}")

# 检查状态
print(f"\n状态检查:")
print(f"state_pos: {board.state_pos}")
print(f"state_statu: {board.state_statu}")

# 检查各个位置
print(f"\n各个位置检查:")
for idx in range(9):
    has_pos = board.state_pos & board.mask_sets[idx]
    has_statu = board.state_statu & board.mask_sets[idx]
    player = 1 if has_statu else (2 if has_pos and not has_statu else 0)
    print(f"位置{idx}: 有棋子={has_pos}, 状态={has_statu}, 玩家={player}")

# 检查 format 函数
from app.yly.envs.game.c5.board.base import format
print(f"\nformat 函数测试:")
print(f"format(0): '{format(0)}'")
print(f"format(1): '{format(1)}'")
print(f"format(2): '{format(2)}'")