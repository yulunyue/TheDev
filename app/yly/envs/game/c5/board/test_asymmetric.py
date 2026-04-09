#!/usr/bin/env python3
"""
测试不对称的局面评分
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

# 创建一个不对称的局面：玩家1有优势
print("=== 创建不对称局面 ===")
# 玩家1：横向四连
board.put_chess(0, 1)  # 玩家1
board.put_chess(1, 1)  # 玩家1
board.put_chess(2, 1)  # 玩家1
board.put_chess(3, 1)  # 玩家1

# 玩家2：只有两个分散的棋子
board.put_chess(7, 2)  # 玩家2
board.put_chess(13, 2)  # 玩家2

# 显示棋盘
print("棋盘状态:")
for line in board.to_str({}):
    print(line)

# 评估局面
print("\n=== 局面评估 ===")
player1_score = board.evaluate_board(1)
player2_score = board.evaluate_board(2)

print(f"玩家1总评分: {player1_score}")
print(f"玩家2总评分: {player2_score}")
print(f"评分差值: {player1_score - player2_score}")

# 检查谁有优势
if player1_score > player2_score:
    print("玩家1有优势")
elif player2_score > player1_score:
    print("玩家2有优势")
else:
    print("评分相同")

# 获取最佳走法
print("\n=== 最佳走法分析 ===")
best_move1, best_score1, scores1 = board.get_best_move(1)
best_move2, best_score2, scores2 = board.get_best_move(2)

print(f"玩家1最佳走法: 位置{best_move1}, 评分{best_score1}")
print(f"玩家2最佳走法: 位置{best_move2}, 评分{best_score2}")

# 检查是否有必胜走法
print("\n=== 必胜走法检查 ===")
for idx in range(25):
    if not (board.state_pos & board.mask_sets[idx]):
        if board.evaluate_move(idx, 1) >= 100000:
            print(f"玩家1在位置{idx}有必胜走法")
        if board.evaluate_move(idx, 2) >= 100000:
            print(f"玩家2在位置{idx}有必胜走法")