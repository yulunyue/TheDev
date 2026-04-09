# BoardC5 高级功能文档

## 概述

本文档描述了为 `BoardC5` 类添加的高级功能，包括胜负判断、单步评分和局面评分。这些功能使得 BoardC5 成为一个完整的五子棋游戏引擎，支持 AI 对战和局面分析。

## 新增功能概述

### 1. 胜负判断功能

#### 核心方法
- `check_win(idx, player_id)`: 检查在指定位置落子后是否获胜
- `get_winner()`: 获取当前棋盘的获胜者
- `is_game_over()`: 检查游戏是否结束
- `_check_line_win(y, x, dy, dx, player_id)`: 检查某个方向是否达到获胜条件

#### 实现细节
- 支持四个方向的获胜检测：横向、纵向、主对角线、副对角线
- 使用位运算高效检查连续棋子
- 支持自定义获胜条件（连子数）
- 正确处理玩家状态位（玩家1和玩家2的区别）

#### 使用示例
```python
board = BoardC5().load(15, 15, 5)  # 15x15棋盘，五子连线

# 检查某个位置落子后是否会获胜
if board.check_win(112, 1):
    print("玩家1在位置112落子会获胜")

# 获取游戏状态
winner = board.get_winner()
if winner == -1:
    print("游戏进行中")
elif winner == 0:
    print("平局")
else:
    print(f"玩家{winner}获胜")

# 检查游戏是否结束
if board.is_game_over():
    print("游戏已结束")
```

### 2. 单步评分功能

#### 核心方法
- `evaluate_move(idx, player_id)`: 评估在指定位置落子的分数
- `_evaluate_position(idx, player_id)`: 评估某个位置的分数
- `_evaluate_line(y, x, dy, dx, player_id)`: 评估某个方向的分数
- `_get_line_info(y, x, dy, dx, player_id)`: 获取某个方向的棋子信息
- `_score_line_pattern(line_info)`: 根据棋子模式评分

#### 评分标准
- 活四（4个连续棋子，两边有空位）：10000分
- 冲四（4个连续棋子，一边被堵）：1000分
- 活三（3个连续棋子，两边有空位）：1000分
- 眠三（3个连续棋子，一边被堵）：100分
- 活二（2个连续棋子，两边有空位）：100分
- 眠二（2个连续棋子，一边被堵）：10分
- 单子：1分

#### 使用示例
```python
board = BoardC5().load(15, 15, 5)

# 评估某个位置的分数
score = board.evaluate_move(112, 1)
print(f"位置112的评分: {score}")

# 找出所有可走位置的评分
for idx in range(225):
    if not board.state_pos & board.mask_sets[idx]:
        score = board.evaluate_move(idx, 1)
        if score > 0:
            print(f"位置{idx}的评分: {score}")
```

### 3. 局面评分功能

#### 核心方法
- `evaluate_board(player_id)`: 评估整个棋盘对某个玩家的分数
- `get_best_move(player_id)`: 获取最佳走法
- `get_move_scores(player_id)`: 获取所有走法的评分

#### 评分策略
- 遍历所有空位，评估每个位置的分数
- 综合考虑进攻和防守
- 对手的分数权重更高（防守更重要）
- 检测必胜和必败局面

#### 使用示例
```python
board = BoardC5().load(15, 15, 5)

# 评估整个局面
player1_score = board.evaluate_board(1)
player2_score = board.evaluate_board(2)
print(f"玩家1评分: {player1_score}")
print(f"玩家2评分: {player2_score}")

# 获取最佳走法
best_move, best_score, score_dict = board.get_best_move(1)
print(f"最佳走法: 位置{best_move}, 评分{best_score}")

# 获取所有走法评分
score_dict = board.get_move_scores(1)
for (y, x), score in score_dict.items():
    print(f"坐标({y}, {x}): 评分{score}")
```

### 4. 增强的显示功能

#### 核心方法
- `to_str(score)`: 增强的棋盘显示，支持评分显示

#### 新特性
- 在空位显示评分数字
- 支持评分字典参数
- 保持原有的棋子显示格式

#### 使用示例
```python
board = BoardC5().load(15, 15, 5)

# 获取评分
score_dict = board.get_move_scores(1)

# 显示带评分的棋盘
board_str = board.to_str(score_dict)
for line in board_str:
    print(line)
```

## 算法详解

### 胜负判断算法

```python
def check_win(self, idx, player_id):
    if not (self.state_pos & self.mask_sets[idx]):
        return False
    
    y = idx // self.width
    x = idx % self.width
    
    for dy, dx in self.DR:
        if self._check_line_win(y, x, dy, dx, player_id):
            return True
    
    return False
```

### 评分算法

```python
def evaluate_move(self, idx, player_id):
    if self.state_pos & self.mask_sets[idx]:
        return -float('inf')
    
    # 模拟落子
    original_pos = self.state_pos
    original_statu = self.state_statu
    
    self.put_chess(idx, player_id)
    score = self._evaluate_position(idx, player_id)
    
    # 恢复状态
    self.state_pos = original_pos
    self.state_statu = original_statu
    
    return score
```

### 局面评估算法

```python
def evaluate_board(self, player_id):
    opponent_id = 3 - player_id
    
    my_score = 0
    opponent_score = 0
    
    for idx in range(self.size):
        if not (self.state_pos & self.mask_sets[idx]):
            my_move_score = self.evaluate_move(idx, player_id)
            opponent_move_score = self.evaluate_move(idx, opponent_id)
            
            if my_move_score > 0:
                my_score += my_move_score
            if opponent_move_score > 0:
                opponent_score += opponent_move_score
    
    # 防御比进攻更重要
    return my_score - opponent_score * 1.2
```

## 性能优化

### 位运算优化
- 使用位运算高效管理棋盘状态
- 使用掩码快速检查位置状态
- 使用位移动快速计算坐标

### 缓存优化
- 避免重复计算
- 使用临时变量保存中间结果
- 快速恢复状态

### 算法优化
- 提前终止检查
- 限制搜索范围
- 优先级排序

## 测试用例

### 胜负判断测试
```python
def test_win_detection(self):
    # 测试横向三连珠
    board = BoardC5().load(5, 5, 3)
    board.put_chess(0, 1)
    board.put_chess(1, 1)
    board.put_chess(2, 1)
    
    assert board.check_win(0, 1)
    assert board.check_win(1, 1)
    assert board.check_win(2, 1)
    assert board.get_winner() == 1
```

### 评分测试
```python
def test_move_evaluation(self):
    board = BoardC5().load(5, 5, 3)
    board.put_chess(0, 1)
    board.put_chess(1, 2)
    board.put_chess(1, 1)
    
    score = board.evaluate_move(2, 1)
    assert score > 0
    
    score = board.evaluate_move(0, 1)
    assert score == -float('inf')
```

### 局面评估测试
```python
def test_board_evaluation(self):
    board = BoardC5().load(5, 5, 3)
    board.put_chess(0, 1)
    board.put_chess(1, 1)
    board.put_chess(2, 1)
    board.put_chess(3, 2)
    board.put_chess(4, 2)
    
    player1_score = board.evaluate_board(1)
    player2_score = board.evaluate_board(2)
    
    # 对称局面评分相同
    assert player1_score == player2_score
```

## 使用建议

### 1. 基本使用
```python
# 创建棋盘
board = BoardC5().load(15, 15, 5)

# 进行游戏
board.put_chess(112, 1)  # 玩家1落子
board.put_chess(113, 2)  # 玩家2落子

# 检查状态
winner = board.get_winner()
if winner != -1:
    print(f"游戏结束，获胜者: {winner}")
```

### 2. AI 对战
```python
# 简单的AI
def ai_move(board, player_id):
    best_move, best_score, _ = board.get_best_move(player_id)
    return best_move

# 使用AI
move = ai_move(board, 1)
board.put_chess(move, 1)
```

### 3. 局面分析
```python
# 分析局面
score_dict = board.get_move_scores(1)
for (y, x), score in sorted(score_dict.items(), key=lambda x: x[1], reverse=True):
    print(f"坐标({y}, {x}): 评分{score}")
```

## 扩展建议

### 1. 搜索算法
- 实现 MinMax 算法
- 添加 Alpha-Beta 剪枝
- 实现 Monte Carlo Tree Search

### 2. 机器学习
- 使用神经网络评估局面
- 训练 AI 模型
- 实现强化学习

### 3. 性能优化
- 多线程计算
- GPU 加速
- 更高效的位运算

### 4. 功能扩展
- 悔棋功能
- 游戏记录保存
- 图形界面
- 网络对战

## 总结

通过添加胜负判断、单步评分和局面评分功能，BoardC5 类已经发展成为一个完整的五子棋游戏引擎。这些功能不仅支持基本的游戏玩法，还为 AI 对战和局面分析提供了强大的工具。

主要改进包括：
1. **完整的胜负判断**：支持各种获胜场景的检测
2. **智能评分系统**：基于棋形模式的评分算法
3. **局面分析**：全面的局面评估和最佳走法推荐
4. **增强显示**：支持评分显示的可视化界面

这些功能使得 BoardC5 能够支持复杂的游戏场景，为五子棋 AI 的开发提供了坚实的基础。通过进一步的优化和扩展，可以构建出强大的五子棋 AI 系统。