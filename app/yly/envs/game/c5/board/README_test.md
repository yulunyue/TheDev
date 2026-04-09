# BoardC5 测试文档

## 概述

本文档描述了针对 `BoardC5` 类的测试策略和测试用例。`BoardC5` 是一个五子棋游戏的核心棋盘类，负责管理棋盘状态、落子操作和状态转换。

## BoardC5 类设计概述

### 核心功能
- **棋盘初始化**: 设置棋盘大小和获胜条件
- **落子操作**: 支持玩家在指定位置落子
- **状态管理**: 使用位运算高效管理棋盘状态
- **格式化输出**: 将棋盘状态转换为可视化字符串

### 关键属性
- `width`: 棋盘宽度
- `height`: 棋盘高度
- `in_row`: 连子数获胜条件
- `size`: 棋盘总格子数
- `state_pos`: 棋子位置状态
- `state_statu`: 棋子状态信息

### 关键方法
- `load(width, height, in_row)`: 初始化棋盘
- `put_chess(idx, player_id)`: 在指定位置落子
- `set_state(state)`: 设置棋盘状态
- `get_state()`: 获取棋盘状态
- `change_grid(s)`: 通过字符串设置棋盘
- `to_str(score)`: 格式化输出棋盘
- `load_records(records)`: 通过记录加载棋盘

## 测试策略

### 测试目标
1. **功能正确性**: 确保所有方法按预期工作
2. **状态一致性**: 确保状态转换的正确性
3. **边界条件**: 测试各种边界情况
4. **性能测试**: 验证位运算的性能

### 测试环境
- Python 3.6+
- unittest 框架
- pytest 兼容

### 测试分类
1. **单元测试**: 测试单个方法的正确性
2. **集成测试**: 测试方法间的交互
3. **系统测试**: 测试完整的游戏流程
4. **性能测试**: 测试大规模操作的性能

## 测试用例设计

### 1. 初始化测试

#### 测试用例 1.1: 基本初始化
```python
def test_basic_initialization(self):
    """测试基本棋盘初始化"""
    board = BoardC5()
    result = board.load(15, 15, 5)
    
    # 验证返回对象
    self.assertEqual(result, board)
    
    # 验证属性设置
    self.assertEqual(board.width, 15)
    self.assertEqual(board.height, 15)
    self.assertEqual(board.in_row, 5)
    self.assertEqual(board.size, 225)
    
    # 验证掩码设置
    self.assertEqual(board.mask_h, (1 << 15) - 1)
    self.assertEqual(board.mask_full, (1 << 225) - 1)
```

#### 测试用例 1.2: 最小棋盘
```python
def test_minimal_board(self):
    """测试最小棋盘（3x3, 3子连线）"""
    board = BoardC5()
    board.load(3, 3, 3)
    
    self.assertEqual(board.width, 3)
    self.assertEqual(board.height, 3)
    self.assertEqual(board.in_row, 3)
    self.assertEqual(board.size, 9)
    self.assertEqual(board.mask_h, (1 << 3) - 1)
    self.assertEqual(board.mask_full, (1 << 9) - 1)
```

#### 测试用例 1.3: 大棋盘
```python
def test_large_board(self):
    """测试大棋盘（20x20, 5子连线）"""
    board = BoardC5()
    board.load(20, 20, 5)
    
    self.assertEqual(board.width, 20)
    self.assertEqual(board.height, 20)
    self.assertEqual(board.in_row, 5)
    self.assertEqual(board.size, 400)
    self.assertEqual(board.mask_h, (1 << 20) - 1)
    self.assertEqual(board.mask_full, (1 << 400) - 1)
```

### 2. 落子操作测试

#### 测试用例 2.1: 基本落子
```python
def test_basic_put_chess(self):
    """测试基本落子操作"""
    board = BoardC5().load(3, 3, 3)
    
    # 玩家1在中心位置落子
    board.put_chess(4, 1)  # 中心位置索引
    
    # 验证状态变化
    self.assertTrue(board.state_pos & board.mask_sets[4])
    self.assertTrue(board.state_statu & board.mask_sets[4])
    
    # 验证棋盘显示
    board_str = board.to_str({})
    self.assertIn("O", board_str[1])  # 玩家1显示为'O'
```

#### 测试用例 2.2: 玩家交替落子
```python
def test_alternate_players(self):
    """测试玩家交替落子"""
    board = BoardC5().load(3, 3, 3)
    
    # 玩家1落子
    board.put_chess(0, 1)
    self.assertTrue(board.state_pos & board.mask_sets[0])
    self.assertTrue(board.state_statu & board.mask_sets[0])  # 玩家1
    
    # 玩家2落子
    board.put_chess(1, 2)
    self.assertTrue(board.state_pos & board.mask_sets[1])
    self.assertFalse(board.state_statu & board.mask_sets[1])  # 玩家2
    
    # 玩家1再次落子
    board.put_chess(2, 1)
    self.assertTrue(board.state_pos & board.mask_sets[2])
    self.assertTrue(board.state_statu & board.mask_sets[2])  # 玩家1
```

#### 测试用例 2.3: 移除棋子
```python
def test_remove_chess(self):
    """测试移除棋子"""
    board = BoardC5().load(3, 3, 3)
    
    # 放置棋子
    board.put_chess(4, 1)
    self.assertTrue(board.state_pos & board.mask_sets[4])
    
    # 移除棋子
    board.put_chess(4, 0)
    self.assertFalse(board.state_pos & board.mask_sets[4])
    self.assertFalse(board.state_statu & board.mask_sets[4])
```

### 3. 状态管理测试

#### 测试用例 3.1: 状态设置和获取
```python
def test_state_set_get(self):
    """测试状态设置和获取"""
    board = BoardC5().load(3, 3, 3)
    
    # 设置一些棋子
    board.put_chess(0, 1)
    board.put_chess(1, 2)
    
    # 获取状态
    state = board.get_state()
    
    # 创建新棋盘并设置状态
    board2 = BoardC5().load(3, 3, 3)
    board2.set_state(state)
    
    # 验证状态一致性
    self.assertEqual(board.state_pos, board2.state_pos)
    self.assertEqual(board.state_statu, board2.state_statu)
```

#### 测试用例 3.2: 字符串状态转换
```python
def test_string_state_conversion(self):
    """测试字符串状态转换"""
    board = BoardC5().load(3, 3, 3)
    
    # 通过字符串设置状态
    board.change_grid("0|1|2|3|4|5")
    
    # 验证落子顺序和玩家
    # 位置0: 玩家1, 位置1: 玩家2, 位置2: 玩家1, 位置3: 玩家2, 位置4: 玩家1, 位置5: 玩家2
    self.assertTrue(board.state_pos & board.mask_sets[0])
    self.assertTrue(board.state_statu & board.mask_sets[0])  # 玩家1
    
    self.assertTrue(board.state_pos & board.mask_sets[1])
    self.assertFalse(board.state_statu & board.mask_sets[1])  # 玩家2
```

#### 测试用例 3.3: 记录加载
```python
def test_load_records(self):
    """测试通过记录加载"""
    board = BoardC5().load(3, 3, 3)
    
    # 通过记录加载
    records = [0, 1, 2, 3, 4, 5]
    board.load_records(records)
    
    # 验证所有位置都有棋子
    for i in range(6):
        self.assertTrue(board.state_pos & board.mask_sets[i])
        # 验证玩家交替
        expected_player = (i % 2) + 1
        if expected_player == 1:
            self.assertTrue(board.state_statu & board.mask_sets[i])
        else:
            self.assertFalse(board.state_statu & board.mask_sets[i])
```

### 4. 格式化输出测试

#### 测试用例 4.1: 空棋盘格式化
```python
def test_empty_board_format(self):
    """测试空棋盘格式化"""
    board = BoardC5().load(3, 3, 3)
    board_str = board.to_str({})
    
    # 验证棋盘结构
    self.assertEqual(len(board_str), 4)  # 3行棋盘 + 1行坐标
    
    # 验证坐标显示
    self.assertIn("0 1 2", board_str[3])
    
    # 验证空位置显示
    for i in range(3):
        self.assertIn(" ", board_str[i])
```

#### 测试用例 4.2: 有棋子棋盘格式化
```python
def test_board_with_pieces_format(self):
    """测试有棋子棋盘格式化"""
    board = BoardC5().load(3, 3, 3)
    
    # 放置一些棋子
    board.put_chess(0, 1)  # 玩家1 -> 'O'
    board.put_chess(1, 2)  # 玩家2 -> 'X'
    board.put_chess(3, 1)  # 玩家1 -> 'O'
    
    board_str = board.to_str({})
    
    # 验证棋子显示
    self.assertIn("O", board_str[0])  # 位置0
    self.assertIn("X", board_str[1])  # 位置1
    self.assertIn("O", board_str[1])  # 位置3
```

### 5. 边界条件测试

#### 测试用例 5.1: 无效位置
```python
def test_invalid_position(self):
    """测试无效位置处理"""
    board = BoardC5().load(3, 3, 3)
    
    # 测试超出范围的索引
    with self.assertRaises(Exception):
        board.put_chess(-1, 1)
    
    with self.assertRaises(Exception):
        board.put_chess(10, 1)
```

#### 测试用例 5.2: 重复落子
```python
def test_repeated_move(self):
    """测试重复落子"""
    board = BoardC5().load(3, 3, 3)
    
    # 在同一位置多次落子
    board.put_chess(4, 1)
    board.put_chess(4, 2)  # 应该覆盖或允许
    board.put_chess(4, 0)  # 移除棋子
    
    # 验证最终状态
    self.assertFalse(board.state_pos & board.mask_sets[4])
```

### 6. 性能测试

#### 测试用例 6.1: 大规模落子操作
```python
def test_large_scale_operations(self):
    """测试大规模落子操作性能"""
    board = BoardC5().load(15, 15, 5)
    
    # 记录开始时间
    import time
    start_time = time.time()
    
    # 执行大量落子操作
    for i in range(1000):
        board.put_chess(i % 225, (i % 2) + 1)
    
    # 记录结束时间
    end_time = time.time()
    
    # 验证性能（应该在合理时间内完成）
    self.assertLess(end_time - start_time, 1.0)
    
    # 验证状态正确性
    expected_count = min(1000, 225)
    self.assertEqual(board.state_pos.bit_count(), expected_count)
```

#### 测试用例 6.2: 状态序列化性能
```python
def test_state_serialization_performance(self):
    """测试状态序列化性能"""
    board = BoardC5().load(15, 15, 5)
    
    # 设置一些棋子
    for i in range(100):
        board.put_chess(i, (i % 2) + 1)
    
    # 测试状态获取性能
    import time
    start_time = time.time()
    
    for _ in range(1000):
        state = board.get_state()
    
    end_time = time.time()
    
    # 验证性能
    self.assertLess(end_time - start_time, 0.1)
    
    # 验证状态一致性
    self.assertEqual(state.bit_count(), 100)
```

## 测试执行

### 运行方式

#### 使用 unittest
```bash
cd app/yly/envs/game/c5/board
python test_board_c5.py
```

#### 使用 pytest
```bash
cd app/yly/envs/game/c5/board
pytest test_board_c5.py -v
```

#### 测试覆盖率
```bash
cd app/yly/envs/game/c5/board
pytest test_board_c5.py --cov=base.py --cov-report=html
```

### 测试报告

测试执行后将生成详细的测试报告，包括：
- 测试通过/失败统计
- 失败用例的详细信息
- 性能测试结果
- 代码覆盖率报告

## 测试数据

### 测试棋盘配置
```python
# 小棋盘测试
SMALL_BOARDS = [
    (3, 3, 3),   # 3x3, 3子连线
    (5, 5, 3),   # 5x5, 3子连线
    (5, 5, 4),   # 5x5, 4子连线
]

# 标准棋盘测试
STANDARD_BOARDS = [
    (15, 15, 5), # 标准15x15五子棋
    (19, 19, 5), # 标准19x19五子棋
]

# 大棋盘测试
LARGE_BOARDS = [
    (20, 20, 5), # 20x20, 5子连线
    (25, 25, 5), # 25x25, 5子连线
]
```

### 测试用例数据
```python
# 测试落子序列
TEST_SEQUENCES = [
    [],                          # 空序列
    [0],                         # 单子
    [0, 1, 2, 3, 4],             # 横向5子
    [0, 5, 10, 15, 20],          # 纵向5子
    [0, 6, 12, 18, 24],          # 对角线5子
    [4, 3, 2, 1, 0],             # 反向横向5子
    [20, 15, 10, 5, 0],          # 反向纵向5子
    [24, 18, 12, 6, 0],          # 反对角线5子
    list(range(225)),            # 填满棋盘
]
```

## 测试环境配置

### 依赖项
```python
# requirements.txt
pytest>=6.0.0
pytest-cov>=2.10.0
```

### 测试配置
```python
# pytest.ini
[pytest]
testpaths = app/yly/envs/game/c5/board
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## 持续集成

### GitHub Actions 配置
```yaml
# .github/workflows/test.yml
name: Test BoardC5
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest app/yly/envs/game/c5/board/test_board_c5.py -v
```

## 测试维护

### 测试数据管理
- 使用 JSON 文件存储测试数据
- 定期更新测试用例以覆盖新功能
- 维护测试数据的版本控制

### 测试结果分析
- 分析失败测试的共性模式
- 监控测试执行时间的变化
- 跟踪代码覆盖率的趋势

### 测试优化
- 识别并优化慢速测试
- 减少测试间的依赖关系
- 提高测试的独立性和可维护性

## 总结

本测试文档提供了全面的 `BoardC5` 类测试策略，确保了棋盘功能的正确性和性能。通过系统化的测试用例设计，可以有效验证：

1. **初始化逻辑**：棋盘大小和参数设置
2. **落子操作**：玩家交替和棋子管理
3. **状态管理**：状态转换和序列化
4. **格式化输出**：棋盘显示和可视化
5. **边界处理**：异常情况和错误处理
6. **性能表现**：大规模操作的处理能力

测试执行后将提供详细的测试报告，帮助开发团队快速定位和修复问题，确保五子棋系统的稳定性和可靠性。