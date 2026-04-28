# 五子棋功能开发记录

## 已有功能

### 后端 (app/tool/chess_f5.py)
- 棋局管理：创建/保存棋局（name, size, p0, p1）
- AI对战模拟：`simulation`功能让两个AI玩家自动对弈
- 落子接口：`play(name, y, x)` 处理玩家落子
- 搜索接口：`search_name` 搜索棋局名称，`search_algo` 搜索AI算法/玩家

### 前端 (font/src/demo/game/chess.ts)
- 棋盘显示：Grid组件渲染棋盘，黑白棋子显示
- 表单操作：支持选择棋局名称、棋盘规格、玩家
- 回合显示：显示当前回合数和执棋方
- 落子交互：点击棋盘触发落子请求并更新棋盘

### 核心引擎 (app/yly/envs/game/c5/)
- 棋盘状态：位运算高效存储棋局状态
- 支持规格：3x3(3连)、6x6(4连)等可配置
- 胜负判定：`in_row`连子判定，`done`状态标识
- AI算法：gomo885, gomo664, ql等

---

## 本次修改记录

### 1. 后端重构 (game.py -> chess_f5.py)
- 文件重命名：`app/tool/game.py` -> `app/tool/chess_f5.py`
- 新增`FontBd`类：定制表单列显示
- 新增`ROUTE_PATH`：统一路由路径 `/app/chess_f5`
- 新增`search_name`：搜索棋局名称
- 新增`search_algo`：搜索AI算法和玩家（支持`IO_MANAGE.get_users_by_topic`）
- `play`方法：调用`c.save()`保存落子记录

### 2. 数据模型重构 (app/yly/envs/game/c5/db.py)
- 新增`ROUTE_PATH = "/app/chess_f5"`
- `SearchModel`设置`url`：关联搜索接口
  - `name.set_url(f"{ROUTE_PATH}/search_name")`
  - `p0/p1.set_url(f"{ROUTE_PATH}/search_algo")`

### 3. 前端优化 (font/src/demo/game/chess.ts)
- 移除`pro: Progress`组件
- 移除`right_div: Div`组件（改为底部）
- 简化布局：表单 + 棋盘
- `top_form.set_input_width(80)`
- `top_form.set_option({url: "/game/f5chess"})` 简化配置

### 4. Bug修复
- `SearchModel.__init__`添加`self.url = ""`默认值，避免`to_json`报错

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