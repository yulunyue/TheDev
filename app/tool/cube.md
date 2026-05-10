# CubeApi 分析

## 概述

`CubeApi` 是魔方（Rubik's Cube）的后端 API 处理器，位于 `app/tool/cube.py`，继承自 `ApiBase`，路由前缀为 `/cube`。

提供 6 个 API 端点：新建、随机打乱、旋转、求解、获取状态、表单定义。

## 依赖结构

```
app/tool/cube.py  ←──  app/yly/envs/game/cube/
                        ├── model.py    →  CubeState（魔方状态）
                        ├── constant.py →  C（常量配置、转动映射）
                        └── algo.py     →  Al（BFS 求解算法）
```

### 基础框架
- `ApiBase` → `common/util/api/apicall.py` — 公有方法自动注册为 API 端点
- `State` → `common/algo/search/states/state.py` — 状态基类，提供 `bfs()`、`dfs()` 等搜索方法
- `Algo` → `common/algo/search/algo.py` — 算法基类
- `Form` → `common/tool/front/form.py` — 前端表单生成工具

## API 端点

### 1. `new` — 新建魔方
- **参数**: `n=2` — 阶数
- **返回**: 已还原状态（state + grid）

### 2. `random` — 随机打乱
- **参数**: `steps=10` — 打乱步数；`show_process=True` — 是否返回过程
- **逻辑**: 随机选择合法动作执行 N 步
- **返回**: 打乱后的状态 + 过程数组（每步的 axis/layer/rotate/grid）

### 3. `rotate` — 旋转
- **参数**: `state, axis, layer, rotate`
- **逻辑**: 从当前状态枚举所有动作，匹配指定的 axis/layer/rotate 并执行
- **返回**: 新状态 + 动作描述
- **异常**: 动作不存在时抛异常

### 4. `solve` — 求解
- **参数**: `state`
- **逻辑**: 使用 `Al.search_main()` 执行 BFS，从当前状态搜索回初始状态
- **返回**: `solved`、`steps`、`actions`（动作序列）

### 5. `get_state` — 获取状态
- **参数**: `state`
- **返回**: 状态信息

### 6. `to_form_column_view` — 表单定义
- 返回前端 FormColumn 配置（axis/select、layer/select、rotate/select、steps/input）

## 私有方法

### `_state_to_node(s: CubeState) -> Node`
将 `CubeState` 转为 API 返回的 `Node` 结构：
```python
{
    "state": s.state,       # 整数编码状态
    "grid": s.grid,         # 每个格子的颜色索引
    "n": C.n,               # 阶数
    "depth": s.depth,       # 深度
    "game_over": bool,      # 是否已还原
    "colors": C.COLORS      # 颜色映射表
}
```

## 核心数据流

```
用户请求 → POST_API.call() → CubeApi.xxx() → CubeState/Action → Node → JSON 响应
```

状态以整数 `state` 在前后端之间传递，后端通过 `encode_data`/`decode_data` 与 `grid` 数组互转。

## 关键模型

### CubeState（model.py）
- 使用 BIT_SIZE=3 位编码每个格子的颜色（6 种颜色）
- `make_actions()` — 枚举所有可能的旋转动作
- `game_over()` — 判断是否等于 `C.init_mask`
- `new_shape(n)` — 创建已还原魔方
- `bfs()` — 继承自 `State`，BFS 到目标状态

### Ct 常量（constant.py）
- `AXIS_NUM = 3` — X/Y/Z 三条轴
- `SIZE = 6` — 六个面
- `ACTIONS[2]` — 2 阶魔方的转动映射表（每个 (axis, layer) 对应三条环的索引）
- `MOVE_ACTION = [-1, 1, 2]` — 逆时针/顺时针/180度
- `get_converts()` — 计算转动后的新状态掩码

### Al 算法（algo.py）
- `search_main(s)` — 从 s 状态 BFS 到初始状态，返回动作路径

## 当前限制

- **仅支持 2 阶魔方**（SHAPE2=2），`ACTIONS` 字典中只有 n=2 的映射
- 解法使用 BFS，大状态空间下性能有限
