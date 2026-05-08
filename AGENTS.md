# TheDev Agent Instructions

Personal experimental project (Python + Tornado + TypeScript + Rust + C++).

## Commands

### Server
- `python main.py dev` — Tornado web server on port 10001 (default env: dev)
- `python main.py test` — same with test env config
- Config auto-created at `config/setting/{env}.json` if missing
- Server writes PID to `data/proc/{env}.pid`

### Testing
- `python -m pytest tests/` — all tests
- `python tool/pytest.py test <module>` — run test by name (searches `tests/`, then `app/`, then `common/`)
- `python tool/pytest.py test <module> <func>` — specific test function (supports `Class::method`)
- `python tool/pytest.py exec <module> <Class>::<method>` — direct execution without pytest
- `python tool/pytest.py cover` — coverage for `common/` + `app/`, output to `data/coverage/`

### Frontend
- `cd font && npm start` — webpack dev server on port 8080
- `cd font && npm run build` — production build

### Rust / C++
- `cd rust/the_dev && cargo build` / `cargo run`
- C++ in `cpp/` (no formal build commands in repo)

### CLI Tools
- `python tool/<name>.py <method>` — auto-discovers methods via `ToolBase`
- Docs auto-generated at `doc/tool/<name>.md`

## Architecture

- **Entrypoint**: `main.py` → `common/third_util/http.py` (Tornado `Application`)
- **API handlers** in `app/tool/`: inherit `ApiBase`; all public methods auto-register as `/{route}/{method_name}`
- **Module loading**: dynamic via `Module.load_module()` with cache invalidation; config defines `py_modules` with `path` + `modules` dict
- **WebSocket** at `/ws` (`TornadaWebSocketConnectHandler`); pub/sub via `IO_MANAGE` (topics in `C` constants)
- **API dispatch**: `MainHandler.POST_API.call(path, params, envs)`, user context from header `the_dev_user`
- **Task runner**: `TASK_MANAGE` reads `config/setting/task.json`, started in `main.py`
- **Config/business data**: JSON files in `config/setting/` (`user.json`, `task.json`) — gitignored, created on first run

## Testing Conventions

- Test classes can inherit `TestBase` (provides `expect()`, `expect_raise_error()`, `run_all_test()`) or use plain pytest
- `@classmethod setup_class()` for class-level setup
- Use `assert_dict` from `common.util.export` for deep dict comparison
- `MockCf` in `common/mock.py` for competitive programming tests with `oj_run()`

## Key Imports

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

## Gotchas

- All public methods on `ApiBase` subclasses become API endpoints — be deliberate about what's exposed
- Test discovery order is `tests/` → `app/` → `common/`; first match wins
- Gunicorn tests (`test_gunicorn.py`) skipped on Windows
- The `File` utility normalizes paths (`\` → `/`) and caches instances by path
- `common/util/export.py` is the hub — almost everything is re-exported from there
- No linter/formatter/typechecker config in repo
