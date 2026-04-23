# OpenCode Agent Instructions

## Essential Commands

### Running the Application
- `python main.py dev` - Start Tornado web server (default env: dev)
- `python main.py test` - Start with test environment config
- Server writes PID to `data/proc/{env}.pid`

### Testing
- `python -m pytest tests/` - Run all tests
- `python tool/pytest.py test <module_name>` - Run specific test module
- `python tool/pytest.py test <module_name> <function_name>` - Run specific test function
- `python tool/pytest.py cover` - Run tests with coverage report

### Frontend Development
- `cd font && npm start` - Start webpack dev server (port 8080)
- `cd font && npm run build` - Build frontend for production

### Rust Development
- `cd rust/the_dev && cargo build` - Build Rust component
- `cd rust/the_dev && cargo run` - Run Rust component

## Architecture

### Core Components
- **main.py** - Entry point; loads config and starts Tornado server
- **common/util/export.py** - Central exports (File, logger, Module, ApiBase, TestBase)
- **common/third_util/http.py** - Tornado server, WebSocket handler, MainHander with POST_API
- **common/mock.py** - MockCf base class for competitive programming tests
- **common/tool/toolbase.py** - Base class for CLI tools with auto-discovery
- **app/tool/** - API endpoint handlers (api.py, user.py, algo.py, manage.py, game.py)
- **config/setting/{env}.json** - Environment configs with `py_modules` mapping URL paths to classes

### Module Loading
- Modules load dynamically from config `py_modules` sections
- Local modules: `./` (relative to project root)
- External modules: `/huawei/secmaster/csb-hcso-hcsu` (absolute path)
- API registration: `MainHander.POST_API.call(path, params, envs)` routes to registered handlers
- WebSocket: `/ws` endpoint for real-time communication
- User context: `envs[C.THE_DEV_USER]` from request header

### API Development
- API handlers inherit from `ApiBase` in `common/util/api/apicall.py`
- Methods are auto-registered via `ApiCall` system
- Request params parsed as JSON for `application/json` content-type

### Testing Conventions
- Test discovery: `tests/` first, then `app/` and `common/`
- Test classes inherit from `TestBase` or use pytest
- Setup with `@classmethod setup_class()` method
- Use `assert_dict` from `common.util.export` for deep comparison
- Mock system: `MockCf` in `common/mock.py` with `oj_run` for competitive programming

### Tool Development
- Extend `ToolBase` for CLI tools
- Use `ToolBase.run()` for command parsing
- Methods are auto-discovered and callable via `python tool/<name>.py <method>`

## Key Imports

```python
from common.util.export import (
    File, logger, get_log, get_dev_log,
    ApiBase, TestBase, Module,
    assert_dict, Node, C
)
```

## Platform-Specific Notes

### Windows
- Gunicorn tests skipped on Windows
- Path separators: Always use `os.path` to handle `/` vs `\`

## Data Directories
- `data/proc/` - Process ID files (`{env}.pid`)
- `data/coverage/` - Test coverage reports
- `data/log/` - Application logs
- `data/log/diff/` - Test diff output
- `data/tool/` - Tool temp files
- `data/cases/` - Test case data