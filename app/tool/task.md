# TaskManage 任务管理工具

## 概述

`app/tool/task.py` 实现了一个后台任务调度系统，支持定时执行配置化的任务。

## 启动方式

```bash
python app/tool/task.py
```

## 核心类

### TaskManage

继承自 `FormBase` 和 `Task`，提供任务管理和执行能力。

| 属性 | 类型 | 说明 |
|------|------|------|
| `model` | `TaskConfig` | 任务配置模型类 |

## 任务配置 (TaskConfig)

配置文件路径: `config/setting/task.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | StrModel | 任务名称 |
| `fun_path` | StrModel | 执行函数路径 (格式: `模块路径/函数名`) |
| `args` | StrModel | 函数参数 (逗号分隔) |
| `run_model` | DictModel | 运行模式配置 |
| `run_num` | NumberModel | 运行次数统计 |
| `result` | DictModel | 执行结果 |

## 工作流程

1. **初始化**: 调用 `TASK_MANAGE.set_resource("config/setting/task.json").start()`
2. **启动**: 创建后台守护线程运行 `run()` 方法
3. **循环执行**: 每秒检查一次所有任务，调用 `exec()` 执行
4. **持久化**: 每次循环后将任务状态保存到 JSON 文件

## API 方法

| 方法 | 说明 |
|------|------|
| `set_resource(path)` | 设置配置文件路径 |
| `loop()` | 执行一轮所有任务 |
| `run()` | 无限循环执行任务 |
| `start()` | 启动后台线程 |
| `add_task(name, **kw)` | 添加新任务 |

## 任务执行

TaskConfig.exec() 方法:
- 通过 `Module.load_module_object()` 动态加载执行函数
- 记录开始/结束时间
- 捕获异常并记录结果
- 更新运行次数和执行结果

## 继承关系

```
TaskManage
├── FormBase (ApiBase)
│   └── 提供 Web 表单交互能力 (to_table_view, web_submit)
└── Task
    └── 提供后台任务调度能力 (loop, run, start)
```

## 配置示例

```json
{
  "task1": {
    "name": "task1",
    "fun_path": "app/some_module/some_func",
    "args": "arg1,arg2",
    "run_model": {},
    "run_num": 0,
    "result": {}
  }
}
```

## 修改记录

### 2026-05-07
- 创建 `app/tool/task.md` 文档
- 记录 TaskManage 类结构和使用方法