# OpenCode Agent Instructions

## Essential Commands

### Running the Application
- `python main.py dev` - Start Tornado web server on port 9999 (default env: dev)
- `python main.py test` - Start with test environment config
- Server writes PID to `data/proc/{env}.pid`

### Testing
- `python -m pytest tests/` - Run all tests
- `python -m pytest tests/common/` - Run common module tests
- `python tool/pytest.py test <module_name>` - Run specific test module
- `python tool/pytest.py test <module_name> <function_name>` - Run specific test function
- `python tool/pytest.py cover` - Run tests with coverage report
- `python tool/pytest.py exec <module_name> <class::function>` - Execute test function directly

### Frontend Development
- `cd font && npm start` - Start webpack dev server (runs on port 8080)
- `cd font && npm run build` - Build frontend for production

### Rust Development
- `cd rust/the_dev && cargo build` - Build Rust component
- `cd rust/the_dev && cargo run` - Run Rust component

## Architecture

### Core Components
- **main.py** - Entry point that loads config and starts Tornado server
- **common/** - Shared utilities and frameworks
  - `util/export.py` - Central exports (File, logger, Module, API tools)
  - `third_util/http.py` - Tornado server and WebSocket handler
  - `mock.py` - Mock framework for testing (MockCf, oj_run)
  - `tool/toolbase.py` - Base class for CLI tools
  - `constant.py` - Application constants (C, THE_DEV_CONSTANT)
- **app/tool/** - API endpoints (api.py, user.py, algo.py, manage.py, game.py)
- **config/setting/** - Environment configs (dev.json, test.json, etc.)

### Configuration System
- Server config: `config/setting/{env}.json`
  - `py_modules` - Maps URL paths to Python classes
  - `port` - Server port (default: 9999)
- API registration: `common/third_util/http.py` MainHander.POST_API
- WebSocket: `/ws` endpoint for real-time communication

### Module Loading
- Modules load dynamically from config `py_modules` sections
- Local modules: `./` (relative to project root)
- External modules: `/huawei/secmaster/csb-hcso-hcsu` (absolute path)
- All modules must be classes that inherit from ApiBase

### Testing Framework
- Uses pytest with custom wrapper in `common/third_util/py_test_util.py`
- Test discovery: `tests/` or `app/` or `common/` directories
- Mock system: `common/mock.py` provides MockCf base class
- Test output: `data/coverage/` for reports
- Test files can use `TestBase` from `common/util/test.py` for custom assertions

### Frontend
- TypeScript/webpack build in `font/` directory
- Websocket connection: `ws://localhost:9999/ws`
- Development server: `http://localhost:8080?route=dyn`

### Rust Integration
- Rust component in `rust/the_dev/` (random/distr libraries)
- Can be called from Python via FFI or subprocess

## Key Conventions

### API Development
- API handlers are classes in `app/tool/` directory
- Use `@ApiBase` decorator or inherit from `ApiBase`
- Methods are auto-registered via `ApiCall` system
- Environment: `envs[C.THE_DEV_USER]` from request header

### Testing Conventions
- Test classes inherit from `TestBase` or use pytest
- Setup with `@classmethod setup_class()` method
- Use `assert_dict` from `common.util.export` for deep comparison
- Tests search in `tests/` first, then `app/` and `common/`

### Logging
- Logger: `logger = get_log("module_name")` from `common.util.export`
- Development log: `logger.info()` writes to console
- Test log: `get_dev_log()` writes to `data/log/diff/`

### File Operations
- File class: `File(path)` from `common.util.export`
- Methods: `read_file()`, `write_file()`, `list_dir()`, `exists()`
- Temp files: `ToolBase.get_temp_file(name)` creates under `data/tool/`

### Tool Development
- Extend `ToolBase` for CLI tools
- Use `Toolbase.run()` for command parsing
- Methods are auto-discovered and callable via `python tool/<name>.py <method>`

## Dependencies

### Python (require.txt)
- `tornado` - Web server framework
- `pytest` - Testing framework
- `coverage` - Code coverage
- `gunicorn` - WSGI server (Linux only)
- `requests` - HTTP client
- `mysql` - MySQL client
- `pyyaml` - YAML parsing
- `sortedcontainers` - Data structures

### Frontend (font/package.json)
- `webpack` - Module bundler
- `typescript` - TypeScript compiler
- `dagre-d3` - Graph visualization
- `mermaid` - Diagram generation
- `panzoom` - Zoom/pan library

### Rust (rust/the_dev/Cargo.toml)
- `rand` - Random number generation
- `rand_distr` - Statistical distributions

## Platform-Specific Notes

### Windows
- Gunicorn tests skipped on Windows (see `common/third_util/test_gunicorn.py`)
- PID file: `data/proc/{env}.pid` (raw process ID)
- Path separators: Always use `os.path` to handle `/` vs `\`

### Linux
- Gunicorn available for production deployment
- PAM/unix socket support if needed

## Data Directories
- `data/proc/` - Process ID files (`{env}.pid`)
- `data/coverage/` - Test coverage reports
- `data/log/` - Application logs
- `data/tool/` - Tool temp files
- `data/cases/` - Test case data