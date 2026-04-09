#!/usr/bin/env python3
"""
调试 _check_line_win 方法
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

# 创建横向三连珠
print("创建横向三连珠")
board.put_chess(0, 1)  # 玩家1在(0,0)
board.put_chess(1, 1)  # 玩家1在(0,1)
board.put_chess(2, 1)  # 玩家1在(0,2)

# 显示棋盘
print("棋盘状态:")
for line in board.to_str({}):
    print(line)

# 测试横向检测
print("\n=== 测试横向检测 ===")
idx = 1  # 中间的棋子
y = idx // 5
x = idx % 5
print(f"测试位置{idx} 坐标({y}, {x})")

for dy, dx in board.DR:
    result = board._check_line_win(y, x, dy, dx, 1)
    print(f"方向({dy}, {dx}): {result}")

# 详细检查横向方向
print(f"\n详细检查横向方向(0, 1):")
dy, dx = 0, 1

# 正向检查
ny, nx = y + dy, x + dx
print(f"正向检查: 从({y}, {x})开始")
while 0 <= ny < 5 and 0 <= nx < 5:
    check_idx = ny * 5 + nx
    has_piece = board.state_pos & board.mask_sets[check_idx]
    player = "无" if not has_piece else ("1" if board.state_statu & board.mask_sets[check_idx] else "2")
    print(f"  位置{check_idx} 坐标({ny}, {nx}): 有棋子={has_piece}, 玩家={player}")
    
    if has_piece:
        if (board.state_statu & board.mask_sets[check_idx]) == 1:  # 玩家1
            print(f"    -> 玩家1棋子，计数+1")
        else:
            print(f"    -> 玩家2棋子，停止检查")
            break
    else:
        print(f"    -> 空位，停止检查")
        break
    
    ny += dy
    nx += dx

# 反向检查
ny, nx = y - dy, x - dx
print(f"反向检查: 从({y}, {x})开始")
count = 1  # 包括当前位置
while 0 <= ny < 5 and 0 <= nx < 5:
    check_idx = ny * 5 + nx
    has_piece = board.state_pos & board.mask_sets[check_idx]
    player = "无" if not has_piece else ("1" if board.state_statu & board.mask_sets[check_idx] else "2")
    print(f"  位置{check_idx} 坐标({ny}, {nx}): 有棋子={has_piece}, 玩家={player}")
    
    if has_piece:
        if (board.state_statu & board.mask_sets[check_idx]) == 1:  # 玩家1
            print(f"    -> 玩家1棋子，计数+1 (当前计数: {count + 1})")
            count += 1
        else:
            print(f"    -> 玩家2棋子，停止检查")
            break
    else:
        print(f"    -> 空位，停止检查")
        break
    
    ny -= dy
    nx -= dx

print(f"\n总棋子数: {count}")
print(f"需要连珠数: {board.in_row}")
print(f"是否获胜: {count >= board.in_row}")