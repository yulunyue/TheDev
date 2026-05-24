# TheDev 智能体指令

语言：中文（所有回复默认使用中文）
个人实验项目（Python + Tornado + TypeScript + Rust + C++）。

## 命令

### 服务器
- `python -m tool.cli dev` — 启动/重启 Tornado Web 服务器，端口由 `config/setting/{env}.json` 配置（dev 环境）；修改后端代码后需重启生效，直接执行此命令，不再预先 ps 检查进程状态

### 测试
- `python -m pytest tests/` — 运行全部测试
- `python tool/pytest.py test <module>` — 按名称运行测试（依次搜索 `tests/`、`app/`、`common/`）
- `python tool/pytest.py test <module> <func>` — 运行指定测试函数（支持 `Class::method` 格式）
- `python tool/pytest.py exec <module> <Class>::<method>` — 直接执行（绕过 pytest）
- `python tool/pytest.py cover` — 对 `common/` + `app/` 生成覆盖率报告，输出到 `data/coverage/`

### 前端
- `cd font && nohup npm run start > ../data/tmp/font.log 2>&1 &` — webpack 开发服务器，端口 8080
- `cd font && npm run build` — 生产构建
- `cd font && npm test` — Vitest 运行测试（`vitest run`）
- `cd font && npm run test:watch` — Vitest 监听模式
- 测试文件以 `.test.ts` / `.spec.ts` 结尾，放在 `src/` 下与被测文件同目录

### Rust / C++
- `cd rust/the_dev && cargo build` / `cargo run`
- C++ 代码在 `cpp/` 目录下（仓库中无正式构建命令）


### CI/CD 发布（Bolun 现网）
- `python -m tool.service.cli bolun_cicd` — **一键发布现网**，依次执行：
  1. `npm_build` — 前端构建
  2. `package` — 打包（`font/dist` + `common` + `app/tool` + `app/yly` + `tool` + `main.py` + `config/setting/production.json`）
  3. `upload_base_64` — 分片上传到 `1.14.97.154:10001`
  4. `install` — 远端解压安装
  5. `restart production` — 远端以 `production` 配置重启
- 可单独执行：`bolun_package` / `bolun_upload` / `bolun_install` / `bolun_restart`
- 配置定义在 `doc/tool/service/cli.md`

## 架构

- **入口**：`main.py` → `common/third_util/http.py`（Tornado `Application`）
- **API 处理器**在 `app/tool/`：继承 `ApiBase`；所有公有方法自动注册为 `/{route}/{method_name}`
- **模块加载**：通过 `Module.load_module()` 动态加载，支持缓存失效；配置文件中使用 `py_modules`，包含 `path` + `modules` 字典
- **WebSocket** 位于 `/ws`（`TornadaWebSocketConnectHandler`）；通过 `IO_MANAGE` 发布/订阅（主题定义在 `C` 常量中）
- **API 分发**：`MainHandler.POST_API.call(path, params, envs)`，用户上下文来自请求头 `the_dev_user`
- **任务执行器**：`TASK_MANAGE` 读取 `config/setting/task.json`，在 `main.py` 中启动
- **配置/业务数据**：JSON 文件存放在 `config/setting/`（`user.json`、`task.json`）— 已加入 gitignore，首次运行时自动创建

## 测试约定

- 测试类可继承 `TestBase`（提供 `expect()`、`expect_raise_error()`、`run_all_test()`）或直接使用 pytest
- 使用 `@classmethod setup_class()` 进行类级别初始化
- 使用 `common.util.export` 中的 `assert_dict` 进行深度字典比较
- `common/mock.py` 中的 `MockCf` 用于竞赛编程测试，配合 `oj_run()` 使用
- 测试文件以 `test_` 开头，统一放在 `tests/` 目录下（如 `foo.py` 的测试写在 `tests/test_foo.py` 或 `tests/foo_test.py`）

## 关键导入

```python
from common.util.export import (
    File, logger, get_log, get_dev_log,
    ApiBase, TestBase, Module,
    assert_dict, Node, C
)
from common.tool.export import (
    ToolBase, PyUtil, System, FrontTable, GC, ProcessLock
)
```

## 两个 export 的分工

| 文件 | 作用域 | 典型导出 |
|---|---|---|
| `common/util/export.py` | **util 层内部**（底层工具） | `File`, `logger`, `Node`, `ApiBase`, `C`, `TestBase`, `Module` 等 |
| `common/tool/export.py` | **tool 层内部**（上层工具） | `GC`, `OsUtil`, `ToolBase`, `System`, `ProcessLock`, `PyUtil`, `FrontTable` 等 |

`util/export.py` 不导出 `tool` 层的类（如 `GC`），反之亦然。需要哪个层的类就从对应的 `export` 导入。

## 前端规范

### 组件生命周期

构造函数中按以下顺序调用，子类覆盖对应方法：
1. `init_node()` — 创建并添加子组件（`this.add_child(new Xxx())`）
2. `init_style()` — 设置样式（`this.set_style({...})`）
3. `init_event()` — 绑定事件回调（`this.input.on_click(...)`）

### 方法职责

- 组件及子组件的构造（创建 DOM 节点）统一放在 `init_node` 函数中（**禁止**在其中调用 `set_style`）
- 组件及子组件的样式统一放在 `init_style` 函数中（所有 `set_style` 调用集中于此）
- **覆盖 `init_style` 时必须调用 `super.init_style()`**，确保父类基础样式（如 FlexDiv 的 `display: flex`）生效
- 组件及子组件的事件绑定统一放在 `init_event` 函数中
- 数据设置统一使用 `set_option(option: Node)` 方法，内部调用 `this.option.set_option(option)` 合并数据，然后调用 `this.render_option()`
- 渲染更新统一放在 `render_option()` 方法中，从 `this.option` 读取数据更新 DOM
- **路由组件**（在 `app.ts` 中注册，如 `AgentMain`、`TaskMain`）覆盖 `render()` 做挂载后的一次性初始化（`app.ts` 中 `mount().render()` 调用链）。**基础组件**（`Search`、`Input`、`Pre` 等）覆盖 `render_option()` 做数据驱动的响应式渲染，由 `set_option()` 自动触发。两者分工不同，互不替代
- `set_option` 返回 `this` 以支持链式调用
- 取值/设值使用 `get_value()` / `set_value()`，变化通知使用 `on_change(cb)` / `do_change(key, src, dst)`
- `FlexColumn` 是垂直方向布局（`flexDirection: column`），`FlexRow` 是水平方向布局（`flexDirection: row`）
- **已删除 `Row` 和 `Column` 别名**，代码中直接使用原名避免命名混淆

### 前后端数据约定

后端 API 返回值统一使用 `Node`，前端解析规则：
- 列表 → `Node(children=[...])` → 前端 `this.children`
- 字典 → `Node(data={...})` → 前端 `.get_data()`
- 标量 → `Node(value=...)` → 前端 `.get_value()`
- 组件 → `Node(type="组件类型", children=[...])` → 前端根据 `type` 渲染对应组件

**Node.type 使用规则**：
- **WebSocket/Agent 消息协议**：必须设置 `type`，使用 `C.MSG_xxx` 常量（定义在 `common/constant.py`）
- **API 返回组件数据**：必须设置 `type`，使用组件类型字符串（如 `"form_row"`、`"table"`）
- **API 返回纯数据**：不设置 `type`，前端通过 `.get_value()` / `.get_data()` 获取数据

## 代码规范

- **一个文件最好只有一个类**（前后端均适用）
- 类名与文件名保持一致（如 `class WebDom` 放在 `web_dom.ts`）
- **Python 代码统一使用 Black 格式化**（配置见 `pyproject.toml`），行长度 88

## Node.type 字段使用指南

`Node.type` 用于标识数据类型，指导前端如何处理数据：

### 后端构造规则

| 场景 | type 设置 | 示例 |
|------|----------|------|
| **消息协议** | 必须设置，用 `C.MSG_xxx` | `Node(type=C.MSG_REGISTER, value=agent_id)` |
| **组件数据** | 必须设置，用组件类型字符串 | `Node(type="form_row", children=[...])` |
| **纯数据返回** | 不设置 type | `Node(value=result)` 或 `Node(data={key: val})` |

### 前端处理规则

- **WebSocket 消息**：根据 `obj.type` 分发到对应回调函数
- **组件渲染**：`DivFactory.new_div(option.type, option.key)` 创建对应组件
- **纯数据**：`.get_value()` 获取标量，`.get_data()` 获取字典

> **⚠️ 语言差异**：Python `Node` 构造函数接受关键字参数 `Node(key=value)`，TypeScript `Node` 构造函数只接受 `key?: string`。TS 端设置多个属性应链式调用 `.set_option({key1: val1, key2: val2})` 或在 `Div.set_option()` 中直接传入纯对象。

### 常见 type 值

| 类别 | type 值 | 说明 |
|------|--------|------|
| 消息协议 | `C.MSG_REGISTER` / `C.MSG_EXEC` 等 | Agent/WebSocket 通信 |
| 表单组件 | `"form"` / `"form_row"` / `"form_column"` | 表单布局 |
| 数据组件 | `"table"` / `"input"` / `"select"` | 数据展示/输入 |
| 布局组件 | `"row"` / `"column"` | Flex 布局容器 |

### Node 顶层字段

以下字段直接位于 `Node` 顶层（不嵌套在 `data` 中），前后端通用：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `ok` | `bool` / `None` | API 调用状态，成功为 `True`，失败为 `False` | `Node(ok=True)` / `Node(ok=False, title="...")` |
| `title` | `str` | **前端元素显示文本/标签**，通用显示字段；`ok=False` 时可填充描述在前端展示 | `Node(ok=False, title="agent not found")` |
| `type` | `str` | 数据类型标识 | `Node(type=C.MSG_EXEC)` |
| `key` | `str` | 唯一标识 | `Node(key=uid(16))` |
| `value` | `any` | 标量值 | `Node(value=result)` |
| `data` | `dict` | 结构化数据 | `Node(data={"k": "v"})` |
| `children` | `list` | 子节点列表 | `Node(children=[...])` |

> **前端访问**：`web_dom.post` 回调收到的是 `JSON.parse` 后的纯对象，顶层字段直接通过 `data.ok`、`data.title` 访问。

### 常量定义文件

- **Python 后端**：`common/constant.py` → `C = Constant()`
- **TypeScript 前端**：`font/src/base/web/constant.ts` → `Constant`

## 全局规则

- **临时文件统一使用 `data/tmp/`**（在项目工作区内，无需额外授权），禁止使用 `/tmp/`
- 所有 shell 命令的输出重定向、临时缓存等均写入 `data/tmp/` 下

- AI 生成前端代码时，必须按 AGENTS.md 规范检查生命周期方法顺序、属性命名、方法职责

## 注意事项

- `ApiBase` 子类中的所有公有方法都会成为 API 端点 — 注意控制暴露范围
- 测试查找顺序为 `tests/` → `app/` → `common/`；优先匹配第一个找到的
- `File` 工具类会规范化路径（`\` → `/`）并按路径缓存实例
- `common/util/export.py` 是 **util 层内部**的枢纽模块，`common/tool/export.py` 是 **tool 层内部**的枢纽模块，互不交叉
- Python 格式化：`black .`（配置在 `pyproject.toml`）


