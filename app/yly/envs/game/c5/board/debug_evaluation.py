#!/usr/bin/env python3
"""
调试评分系统
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

# 玩家1占据优势（横向三连）
print("=== 创建棋盘局面 ===")
board.put_chess(0, 1)  # 玩家1
board.put_chess(1, 1)  # 玩家1
board.put_chess(2, 1)  # 玩家1

# 玩家2有一些分散的棋子
board.put_chess(3, 2)  # 玩家2
board.put_chess(4, 2)  # 玩家2

# 显示棋盘
print("棋盘状态:")
for line in board.to_str({}):
    print(line)

# 分析各个位置的评分
print("\n=== 分析各个位置的评分 ===")

# 玩家1的评分
print("玩家1的各个位置评分:")
for idx in range(25):
    if not (board.state_pos & board.mask_sets[idx]):
        score = board.evaluate_move(idx, 1)
        y = idx // 5
        x = idx % 5
        if score > 0:
            print(f"  位置{idx} 坐标({y}, {x}): {score}")

# 玩家2的评分
print("\n玩家2的各个位置评分:")
for idx in range(25):
    if not (board.state_pos & board.mask_sets[idx]):
        score = board.evaluate_move(idx, 2)
        y = idx // 5
        x = idx % 5
        if score > 0:
            print(f"  位置{idx} 坐标({y}, {x}): {score}")

# 评估局面
print("\n=== 局面评估 ===")
player1_score = board.evaluate_board(1)
player2_score = board.evaluate_board(2)

print(f"玩家1总评分: {player1_score}")
print(f"玩家2总评分: {player2_score}")

# 获取最佳走法
print("\n=== 最佳走法分析 ===")
best_move1, best_score1, scores1 = board.get_best_move(1)
best_move2, best_score2, scores2 = board.get_best_move(2)

print(f"玩家1最佳走法: 位置{best_move1}, 评分{best_score1}")
print(f"玩家2最佳走法: 位置{best_move2}, 评分{best_score2}")