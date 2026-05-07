# chess_f5 前后端架构文档

> 此文档用于指导代码修改，修改此文档后可让 AI 理解变更需求

## 目录结构

```
app/
├── tool/
│   ├── chess_f5.py          # API 入口层
│   └── chess_f5_test.py     # API 测试
└── yly/envs/game/c5/
    ├── db.py                 # 数据模型 (Bd)
    ├── board/base.py         # 棋盘逻辑 (BoardC5)
    ├── model/
    │   ├── chess_state.py    # 游戏状态 (CState664, CState333)
    │   ├── chess_state_map.py # 状态映射 (CHESS_MAP_CLS_FUNC)
    │   └── chess_action.py   # 动作定义 (ChessACtion)
    └── player/
        ├── al.py             # AI 算法管理器 (Al)
        ├── ql.py             # Q-Learning 玩家 (Ql)
        └── gm_player.py      # AlphaZero Gomoku 玩家 (GmuMo)

font/src/
└── demo/game/
    └── chess.ts              # 前端 UI (Chess)
```

---

## 后端架构

### API 层: `app/tool/chess_f5.py`

**路由**: `/game/f5chess`

**继承**: `FormBase` + `ApiBase`

**类**: `ChessF5`

**方法**:
| 方法 | 功能 | 请求示例 |
|------|------|----------|
| `search_name` | 搜索棋局名称列表 | POST `/game/f5chess/search_name` |
| `search_algo` | 搜索 AI 玩家列表 | POST `/game/f5chess/search_algo` |
| `get` | 获取棋局数据 | POST `/game/f5chess/get` `{key: "棋局名"}` |
| `play` | 下棋操作 | POST `/game/f5chess/play` `{name, y, x}` |
| `web_submit` | 提交棋局 | POST `/game/f5chess/web_submit` `{type: "save"|"simulation", value}` |
| `to_form_column_view` | 返回表单视图配置 | POST `/game/f5chess/to_form_column_view` |

**关键变量**:
- `AI_PLAYER = {"ad3", "mc100"}` - 只有这两个玩家可执行模拟
- `ROUTE_PATH = "/game/f5chess"` - 路由路径

---

### 数据模型: `app/yly/envs/game/c5/db.py`

**类**: `Bd` 继承 `FileConfig`

**字段定义**:
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | SearchModel | "default" | 棋局名称，搜索 URL: `/game/f5chess/search_name` |
| `size` | SelectModel | "C333" | 棋盘尺寸，选项: `C333`, `C664` |
| `records` | ListModel | [] | 落子记录 (idx 列表) |
| `p0` | SearchModel | "ad3" | 玩家0，搜索 URL: `/game/f5chess/search_algo` |
| `p1` | SearchModel | "ad3" | 玩家1，搜索 URL: `/game/f5chess/search_algo` |

**方法**:
- `get_id(name)` → 返回 `str(name)`
- `get_state()` → 根据 `size` 和 `records` 生成棋盘状态对象
- `get_form_columns()` → 返回 `[size, p0, p1]`
- `to_json()` → 返回 `{name, size, records, p0, p1, width, height}`

**存储位置**: `data/game/chess.json`

---

### 棋盘逻辑: `app/yly/envs/game/c5/board/base.py`

**类**: `BoardC5`

**核心方法**:
| 方法 | 功能 |
|------|------|
| `load(width, height, in_row)` | 初始化棋盘参数 |
| `yx_to_idx(y, x)` | 坐标转索引: `x * height + y` |
| `get_yx(idx)` | 索引转坐标: `idx % height`, `idx // height` |
| `set_state(state)` | 设置状态 (位运算) |
| `get_state()` | 获取状态值 |
| `put_chess(idx, player_id)` | 在位置落子 (player_id: 1=黑, 2=白) |
| `load_records(records)` | 从落子记录加载棋盘 |
| `get_can_moves()` | 获取可落子位置 |
| `to_str()` | 打印棋盘字符串 |

**位运算说明**:
- `state_pos`: 位置掩码 (哪些位置有棋子)
- `state_statu`: 状态掩码 (区分黑白)
- `state = (state_pos << size) | state_statu`

---

### 游戏状态: `app/yly/envs/game/c5/model/chess_state.py`

**类**: `CState664` 继承 `AbState`

**属性**:
| 属性 | 值 | 说明 |
|------|-----|------|
| `w` | 6 | 宽度 |
| `h` | 6 | 高度 |
| `in_row` | 4 | 连子获胜数 |
| `name` | "C664" | 标识名 |

**类**: `CState333` 继承 `CState664`

**属性**:
| 属性 | 值 | 说明 |
|------|-----|------|
| `w` | 3 | 宽度 |
| `h` | 3 | 高度 |
| `in_row` | 3 | 连子获胜数 |
| `name` | "C333" | 标识名 |

**状态映射**: `CHESS_MAP_CLS_FUNC = {"C664": CState664, "C333": CState333}`

---

### AI 玩家: `app/yly/envs/game/c5/player/al.py`

**类**: `Al` 继承 `ALgoManage`

**可用玩家**:
| 方法 | 玩家名 | 说明 |
|------|--------|------|
| `gomo885()` | "gomo885" | 8x8x5 模型 |
| `gomo664()` | "gomo664" | 6x6x4 模型 |
| `gomo664_1500()` | "gomo664_1500" | 训练模型 |
| `ql()` | "ql" | Q-Learning 玩家 |

---

## 前端架构

### UI 组件: `font/src/demo/game/chess.ts`

**类**: `Chess` 继承 `Column`

**组件结构**:
```
Column (Chess)
├── Div (left_div)
├── Row (mid_main)
│   ├── Column (head_column)
│   │   ├── Search (name_search) - 搜索棋局名称
│   │   └── Title (title) - 显示回合信息
│   ├── Grid (g) - 棋盘网格 (SVG)
│   └── FormColumn (bottom_form) - 底部表单
└── Div (right_div)
```

**交互事件**:
| 事件 | 触发 | 请求 |
|------|------|------|
| `name_search.on_change` | 选择棋局名称 | POST `/game/f5chess/get` `{key: name}` |
| `g.on_click` | 点击棋盘格子 | POST `/game/f5chess/play` `{name, y, x}` |
| `bottom_form.render` | 加载表单 | POST `/game/f5chess/to_form_column_view` |

---

## 数据流

```
前端                              后端
────────────────────────────────────────────────────
选择棋局名称
  ↓ web_dom.post("/game/f5chess/get", {key})
                          ↓ ChessF5.get(key)
                          ↓ Bd.get(key).to_json()
  ↓ show_data(dst)        ↑ {p0, p1, records, width, height}
  ↓ Grid.set_option()     ↑ 绘制棋盘

点击棋盘格子
  ↓ web_dom.post("/game/f5chess/play", {name, y, x})
                          ↓ ChessF5.play()
                          ↓ BoardC5.yx_to_idx(y, x)
                          ↓ 验证 idx in can_moves
                          ↓ records.append(idx)
                          ↓ Bd.save()
                          ↓ IO_MANAGE.send() (WebSocket广播)
  ↓ show_data(data)       ↑ 更新棋盘显示
```

---

## 测试要点

**文件**: `app/tool/chess_f5_test.py`

**关键测试**:
- `test_route_path`: 验证路由 `/game/f5chess`
- `test_ai_player_set`: 验证 `AI_PLAYER = {"ad3", "mc100"}`
- `test_cstate664_attributes`: 验证 `w=6, h=6, in_row=4`
- `test_cstate333_attributes`: 验证 `w=3, h=3, in_row=3`
- `test_get_can_moves_empty`: 空 6x6 棋盘有 36 个可落子位置
- `test_web_submit_simulation_non_ai`: 非AI玩家不可模拟

---

## 待完成功能

| 优先级 | 功能 | 说明 |
|--------|------|------|
| **高** | 胜负判定提示 | 游戏结束时显示胜负结果 |
| **高** | 落子有效性检查 | 前端禁止点击已有棋子的位置 |
| **中** | 人机对战 | 人类玩家vs AI自动回应 |
| **中** | 悔棋功能 | 撤销上一步操作 |
| **中** | 新建棋局 | 前端创建新棋局入口 |
| **低** | 观战模式 | WebSocket实时推送棋局变化 |
| **低** | 复盘功能 | 回放历史棋局 |

---

## 变更记录

> 在此记录需要修改的内容，AI 将根据此部分修改代码

### 待修改项

(在此添加修改需求)

### 已完成项

#### 2024-05-07: WebSocket 观战订阅机制
**前端修改 (用户)**:
- `chess.ts`: 切换棋局时订阅 `{TOPIC_TASK_UPDATE_MSG}.{棋局名}` 主题
- `show_data()`: 开始时调用 `bottom_form.set_value(dst)` 同步表单

**后端适配**:
- `common/constant.py`: 添加 `METHOD_UN_SUB = "un_sub"`
- `common/util/io/manage.py`: `Manage.un_sub()` 方法取消订阅
- `app/tool/chess_f5.py`: `play()` 推送到 `{TOPIC_TASK_UPDATE_MSG}.{name}` 主题，数据为完整棋局 `result`

#### 2024-05-07: 胜负判定提示功能
**后端修改**:
- `app/yly/envs/game/c5/db.py`: `Bd.to_json()` 添加 `done` 字段返回
- `app/tool/chess_f5.py`: `play()` 方法返回包含 `done` 状态的 `Node`

**前端修改**:
- `font/src/demo/game/chess.ts`: `show_data()` 根据 `done` 显示:
  - `done == null`: 显示回合和执棋方
  - `done == "NO_WIN"`: 显示平局
  - `done == "1"` 或 `"2"`: 显示获胜玩家