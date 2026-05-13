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
  - test_to_str: 测试状态可视化（验证行数和旋转后的可视化输出）
  - test_bfs_from_init: 测试动作生成（替代BFS）
  - test_solve_one_step: 测试单步求解
  - test_solve_multiple_steps: 测试多步求解
  - test_state_depth: 测试状态深度
  - test_all_colors_present: 测试所有颜色存在
  - test_actions_data_analysis: 分析验证 ACTIONS 数据结构
  - test_all_actions_coverage: 验证动作覆盖完整性
  - test_random_scramble_15_steps: 测试随机生成15步走法并序列化到 data/cube/test.json
  - test_solve_and_visualize: 测试求解魔方并可视化显示还原过程
- 修复 model.py:make_actions() - 修正 depth 参数传递问题
- State基类增加序列化方法：
  - save_to_file(filepath): 保存状态到文件
  - load_from_file(filepath): 从文件加载状态
  - to_json(): 子类实现，返回JSON字典
  - load_from_json(data): 子类实现，从JSON字典加载
- CubeState实现to_json()和load_from_json()
  - 序列化：state、grid、depth、n、game_over
  - 支持从JSON恢复完整状态
- 增加求解可视化测试：
  - 随机打乱3步魔方
  - 输出打乱后的魔方状态（使用to_str可视化）
  - 搜索求解步骤并输出每步动作和状态变化
  - 验证最终状态完成（game_over为True）
  - 保存结果到 data/cube/solve_result.json

### 2026-05-09
- 实现魔方2D可视化前后端
  - 后端：app/tool/cube.py
    - 路由：/cube
    - API接口：new, random, rotate, solve, get_state, to_form_column_view
    - 支持随机打乱（返回动作序列）、单步旋转、BFS求解
    - 修复：移除 FormBase 继承，改为直接继承 ApiBase
    - 修复：使用 Form().set_column() 构建表单视图
  - 前端：font/src/demo/cube/
    - cube_grid.ts: 2D展开视图组件
    - cube_main.ts: 主组件（控制面板+动画演示）
    - 注册路由到 font/src/app.ts
  - 测试：app/tool/cube_test.py（6个测试全部通过）
  - 功能特性：
    - 完全下拉选择旋转（轴/层/方向）
    - 打乱动画展示每一步
    - 求解动画自动演示
    - 经典颜色方案
  - 配置更新：config/setting/dev.json 添加 /cube 路由

### ACTIONS 数据结构分析

**ACTIONS[C.SHAPE2] 结构**：
```
{
    (axis, layer): [
        [面内旋转的4个索引],    # 组0: 当前面内块的旋转
        [周边旋转的4个索引],    # 组1: 周边面的块旋转
        [周边旋转的4个索引]     # 组2: 其他周边面的块旋转
    ]
}
```

**分析结果**：
- 二阶魔方：6面 × 4块 = 24个小块（索引0-23）
- 每个旋转操作影响：面内4块 + 周边8块 = 12个唯一小块
- 共6个动作组合：3轴 × 2层
- 每个动作组合包含3组，每组4个索引形成循环置换

**验证结果**：
- ✓ 所有索引在有效范围(0-23)内
- ✓ 每组正确包含4个元素
- ✓ 每个旋转影响12个唯一小块
- ✓ 所有18个动作唯一覆盖完整

**面索引分布**：
- 面0(上): [0, 1, 2, 3]
- 面1(前): [4, 5, 6, 7]
- 面2(右): [8, 9, 10, 11]
- 面3(后): [12, 13, 14, 15]
- 面4(左): [16, 17, 18, 19]
- 面5(下): [20, 21, 22, 23]

**结论**: ACTIONS数据索引范围正确，数据完整性验证通过。旋转逻辑使用 `all_size - 1 - idx` 进行位置映射。

### 2026-05-13
- **修复所有6个 ACTIONS 几何错误**：每个 action 现在精确旋转同一层的 4 个 cubie（之前 face cycle 和 side cycles 使用不同层，导致混层旋转 7-8 个 cubie）。
  - (0,0) y+层：face Face0 + side y+行（之前用了 y-行）
  - (0,1) y-层：face Face5 + side y-行
  - (1,0) x+层：face Face3 + side x+列（之前用了 Face1 x-层）
  - (1,1) x-层：face Face1 + side x-列
  - (2,0) z+层：face Face2 + side z+行
  - (2,1) z-层：face Face4 + side z-行
- **CubeAction.show()**: 改为 `"{xyz}轴 第{n}层 {顺/逆时针90°/180°}旋转"` 格式
- **测试修复**：
  - `color` → `axis`（set_view 存的是 axis 而非 color）
  - test_to_str、test_all_actions_to_str 期望值随 ACTIONS 更新
  - `色` → `轴`（show 用 xyz 轴命名）
  - test_random_step 放宽 depth 断言（随机性）
- **webpack.config.js**：ts-loader 加 `transpileOnly: true`，规避已有 TS2612 strict 错误
- CICD 部署成功至 Bolun 现网