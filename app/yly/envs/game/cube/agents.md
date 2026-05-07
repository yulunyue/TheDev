# Cube 模块 - 魔方求解器

## 概述

该模块实现了一个完整的魔方求解系统，采用分层架构设计，利用位编码和预计算动作表实现高效的状态转换。

## 目录结构

```
app/yly/envs/game/cube/
├── constant.py    # 常量和配置：魔方配置、动作映射、状态转换
├── model.py       # 数据模型：CubeState（状态）、CubeAction（动作）
├── algo.py        # 算法层：BFS求解算法
├── main.py        # 应用层：命令行工具接口
└── main/          # 文档目录
    └── py.md
```

## 核心组件

### 1. constant.py - 配置层

**类 `Ct`**: 魔方配置类

- `SIZE = 6`: 魔方面数
- `SHAPE2 = 2`: 二阶魔方标识
- `AXIS_NUM = 3`: 旋转轴数量（X, Y, Z）
- `BIT_SIZE = 3`: 每个小块状态编码位数
- `COLORS`: 颜色数组 `["红", "黄", "蓝", "绿", "橙", "白"]`
- `ACTIONS`: 预定义的动作映射表，针对二阶魔方的旋转操作
- `MOVE_ACTION = [-1, 1, 2]`: 移动动作类型

**关键方法**:
- `load(n=SHAPE2)`: 初始化魔方配置
- `new_shape_state(n)`: 创建新魔方初始状态（位编码）
- `get_converts(mask, i, j, tp, grid)`: 执行旋转操作

**全局实例**: `C = Ct().load()`

### 2. model.py - 模型层

**类 `CubeAction(Action)`**: 魔方动作
- `show(msg=None)`: 显示动作描述，格式"第X层颜色-顺时针旋转Y圈"

**类 `CubeState(State)`**: 魔方状态
- `grid`: 解码后的魔方状态数组
- `__init__(state, depth=0)`: 初始化并解码状态
- `new_shape(n)`: 类方法，创建指定阶数魔方初始状态
- `game_over()`: 判断是否完成（是否等于初始状态）
- `make_actions()`: 生成所有可能动作（3轴 × n层 × 3种旋转）
- `to_str()`: 将魔方状态转换为可视化字符串数组

**状态编码**: 使用位编码，二阶魔方24个小块，每个3位，共72位

**可视化布局**:
```
      面0（上）
面4 面1 面2 面3（侧面）
      面5（下）
```

### 3. algo.py - 算法层

**类 `Al(Algo)`**: 魔方求解算法
- `search_main(s: CubeState)`: BFS搜索最优解，返回动作序列

**算法特点**:
- 基于BFS广度优先搜索
- 保证最短路径
- 继承自 `common.algo.export.Algo`

### 4. main.py - 应用层

**类 `Solution(ToolBase)`**: 命令行工具
- `name = "cube"`: 工具名称
- `random(step=10)`: 随机打乱魔方step步
- `view_all()`: 查看所有可能动作及结果
- `dev()`: 开发调试方法

**使用方式**:
```bash
python tool/cube.py random 10    # 随机打乱10步
python tool/cube.py view_all     # 查看所有动作
python tool/cube.py dev          # 开发调试
```

## 依赖关系

```
constant.py (无内部依赖)
    ↓
model.py
    ├── constant.py (C 配置)
    ├── common.algo.export (State, Action, encode_data, decode_data)
    └── common.third_util.ml.np_util (np)
    ↓
algo.py
    ├── model.py (CubeState)
    ├── constant.py (C)
    └── common.algo.export (Algo)
    ↓
main.py
    ├── model.py (CubeState, C)
    ├── algo.py (Al)
    └── common.util.export (ToolBase, logger, Module, log)
```

## 架构设计

```
┌─────────────────────────────────────┐
│        应用层 (main.py)              │
│         Solution (ToolBase)         │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│        算法层 (algo.py)              │
│         Al (Algo) - BFS              │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│        模型层 (model.py)             │
│   CubeState (State) / CubeAction     │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│        配置层 (constant.py)          │
│         Ct (常量和转换规则)           │
└─────────────────────────────────────┘
```

## 核心设计

### 状态编码
- 位编码（Bit Encoding）表示魔方状态
- 二阶魔方：6面 × 2×2 = 24小块，每个3位编码
- 总共72位，实际状态空间约3.67×10^6

### 动作系统
- ACTIONS字典：预计算每个旋转操作影响的小块索引
- 运行时查表+位运算，高效

### 求解算法
- BFS保证最优解
- 状态哈希去重
- 适合小规模状态空间

## 使用示例

```python
# 1. 创建魔方状态
s = CubeState.new_shape(C.SHAPE2)

# 2. 打乱魔方
s = s.get_random_action().get_dst()

# 3. 求解
algo = Al()
actions = algo.search_main(s)

# 4. 验证
for a in actions:
    s = a.get_dst()
assert s.game_over()
```

## 扩展性

### 支持不同阶数
- `Ct.load(n)` 加载不同阶数配置
- ACTIONS字典按阶数组织

### 算法可替换
- 继承 `Algo` 基类可实现：
  - IDA*（迭代加深A*）
  - Kociemba 两阶段算法
  - 机器学习方法（DQN等）

---

## 修改记录

### 2026-05-07
- 创建 agents.md 文档，记录模块分析结果
- 增加 test_all.py 测试文件，覆盖以下测试：
  - test_constant: 测试常量配置
  - test_state_new: 测试创建初始状态
  - test_state_make_actions: 测试生成所有动作
  - test_action_show: 测试动作显示
  - test_state_convert: 测试状态转换
  - test_random_action: 测试随机动作
  - test_to_str: 测试状态可视化
  - test_bfs_from_init: 测试动作生成（替代BFS）
  - test_solve_one_step: 测试单步求解
  - test_solve_multiple_steps: 测试多步求解
  - test_state_depth: 测试状态深度
  - test_all_colors_present: 测试所有颜色存在
- 修复 model.py:make_actions() - 修正 depth 参数传递问题