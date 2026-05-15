# TheDev 智能体指令

语言：中文（所有回复默认使用中文）
个人实验项目（Python + Tornado + TypeScript + Rust + C++）。

## 命令

### 服务器
- `python main.py dev` — Tornado Web 服务器，端口 10001（默认环境：dev）
- `python main.py test` — 同上，使用 test 环境配置
- 配置文件自动创建在 `config/setting/{env}.json`（若不存在）
- 服务器将 PID 写入 `data/proc/{env}.pid`
- 重启服务需先 `kill` 旧进程，然后用 `nohup python main.py dev > /dev/null 2>&1 &` 启动（避免 shell 超时后被杀死）
- 前端 `npm start` 需用 `setsid sh -c 'cd font && npm start > data/tmp/frontend.log 2>&1 &'` 启动（`nohup` 对 npm 不可靠）
- 重启前后端后需用 `lsof -i :<port>` 确认端口已监听

### 测试
- `python -m pytest tests/` — 运行全部测试
- `python tool/pytest.py test <module>` — 按名称运行测试（依次搜索 `tests/`、`app/`、`common/`）
- `python tool/pytest.py test <module> <func>` — 运行指定测试函数（支持 `Class::method` 格式）
- `python tool/pytest.py exec <module> <Class>::<method>` — 直接执行（绕过 pytest）
- `python tool/pytest.py cover` — 对 `common/` + `app/` 生成覆盖率报告，输出到 `data/coverage/`

### 前端
- `cd font && npm start` — webpack 开发服务器，端口 8080
- `cd font && npm run build` — 生产构建

### Rust / C++
- `cd rust/the_dev && cargo build` / `cargo run`
- C++ 代码在 `cpp/` 目录下（仓库中无正式构建命令）

### CLI 工具
- `python tool/<name>.py <method>` — 通过 `ToolBase` 自动发现方法
- 文档自动生成在 `doc/tool/<name>.md`

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
- 测试文件以 `_test` 结尾，与源码同目录（如 `foo.py` 的测试写在 `foo_test.py`）

## 关键导入

```python
from common.util.export import (
    File, logger, get_log, get_dev_log,
    ApiBase, TestBase, Module,
    assert_dict, Node, C
)
from common.tool.export import (
    ToolBase, PyUtil, System, FrontTable
)
```

## 前端规范

### 组件生命周期

构造函数中按以下顺序调用，子类覆盖对应方法：
1. `init_node()` — 创建并添加子组件（`this.add_child(new Xxx())`）
2. `init_style()` — 设置样式（`this.set_style({...})`）
3. `init_event()` — 绑定事件回调（`this.input.on_click(...)`）

### 方法职责

- 组件及子组件的构造（创建 DOM 节点）统一放在 `init_node` 函数中（**禁止**在其中调用 `set_style`）
- 组件及子组件的样式统一放在 `init_style` 函数中（所有 `set_style` 调用集中于此）
- 组件及子组件的事件绑定统一放在 `init_event` 函数中
- 数据设置统一使用 `set_option(option: Node)` 方法，内部调用 `this.option.set_option(option)` 合并数据，然后调用 `this.render_option()`
- 渲染更新统一放在 `render_option()` 方法中，从 `this.option` 读取数据更新 DOM
- `set_option` 返回 `this` 以支持链式调用
- 取值/设值使用 `get_value()` / `set_value()`，变化通知使用 `on_change(cb)` / `do_change(key, src, dst)`
- `FlexColumn` 是垂直方向布局（`flexDirection: column`），`FlexRow` 是水平方向布局（`flexDirection: row`）
- **已删除 `Row` 和 `Column` 别名**，代码中直接使用原名避免命名混淆

## 代码规范

- **一个文件最好只有一个类**（前后端均适用）
- 类名与文件名保持一致（如 `class WebDom` 放在 `web_dom.ts`）
- **Python 代码统一使用 Black 格式化**（配置见 `pyproject.toml`），行长度 88

## 全局规则

- **临时文件统一使用 `data/tmp/`**（在项目工作区内，无需额外授权），禁止使用 `/tmp/`
- 所有 shell 命令的输出重定向、临时缓存等均写入 `data/tmp/` 下
- **进程管理使用 `ProcessLock` 类**（`common/tool/func/process_lock.py`）：
  - 所有进程启动前必须检查并关闭同名的旧进程（使用 `ProcessLock(name).start_unique()`）
  - PID 文件存放在 `data/proc/{name}.pid`
  - **执行关闭进程操作前必须手动确认**，避免误杀其他进程（如 opencode 自身）
  - 导入方式：`from common.tool.export import ProcessLock`

## 注意事项

- `ApiBase` 子类中的所有公有方法都会成为 API 端点 — 注意控制暴露范围
- 测试查找顺序为 `tests/` → `app/` → `common/`；优先匹配第一个找到的
- Gunicorn 测试（`test_gunicorn.py`）在 Windows 上跳过
- `File` 工具类会规范化路径（`\` → `/`）并按路径缓存实例
- `common/util/export.py` 是枢纽模块 — 几乎所有内容都从这里重新导出
- Python 格式化：`black .`（配置在 `pyproject.toml`）
