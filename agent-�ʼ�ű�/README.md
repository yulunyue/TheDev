# User-Agentic 数据集自动化质检系统 — 使用说明书

本系统是一款针对大模型 Agent 在软件开发、Bug 修复（Bug-fix）或特性开发（Feature）任务中所生成的**交付数据集**进行全方位质量检验（Quality Check）的自动化工具。它通过解析静态交付文件、调用 Docker 隔离环境构建镜像、进行双阶段回归测试等手段，确保最终交付数据集的高完备性、高真实性及高修复质量。

---

## 📊 11 大核心质检模块 (M1 - M11)

系统内置了 11 个独立的质检指标模块，您可以通过编辑 `quality_check.py` 顶部的全局开关（如 `ENABLE_M1_FILE_COMPLETENESS = True`）来启用或跳过特定检查：

| 模块 ID | 模块名称 | 验证原理与核心内容 | 依赖 Docker |
| :--- | :--- | :--- | :---: |
| **M1** | **文件完备性** | 检查任务交付目录下是否包含必需文件（如 `code.patch`, `test.patch`, `final.diff`, `trajectory.json`, `Dockerfile`, `setup_env.sh`, `setup_repo.sh`, `run_verification.py` ）。同时过滤多余冗余文件，识别并报警 Mac 垃圾残留 `__MACOSX` 文件夹。 | ❌ |
| **M2** | **instance.json 字段校验** | 解析类似 `[owner]__[repo]-[pr_id].json` 的任务定义文件。校验必填字段（如 `instance_id`, `repo`, `base_commit`, `problem_statement`, `FAIL_TO_PASS`, `PASS_TO_PASS`, `patch`, `test_patch` ）的存在性、类型正确性及非空校验。 | ❌ |
| **M3** | **trajectory.json 格式与字段校验** | 检验 Agent 运行轨迹 JSON 的层级字段。分析 `trajectory` 数组，确保对话中的 `role` 链路健全，且 `tool_use` 与 `tool_result` 能够通过 ID 和 Name 成功匹配闭环。 | ❌ |
| **M4** | **Patch 相似度校验** | *(默认禁用)* 比对 `code.patch` 与 `final.diff` 的相似度。 | ❌ |
| **M5** | **提示词泄露检测** | *(默认禁用)* 对 Agent 的输出数据流进行敏感/专有提示词过滤。 | ❌ |
| **M6** | **容器初始状态验证** | 启动 Docker 容器，读取并比对 `trajectory.json` 声明的 `initial_state` 文件及其内容，通过容器内读取匹配，确保物理初始状态完全真实一致。 | **✔️ 是** |
| **M7** | **脚本回归验证** | 挂载任务交付的验证脚本（如 `run_verification.py`）进 Docker 容器执行，验证在交付的测试逻辑下是否能成功 PASS。自动兼容适配 JavaScript 等多语言生态下的测试框架（mocha/jest等）及 NVM 环境。 | **✔️ 是** |
| **M8** | **非依赖脚本回归验证** | **核心高智能模块**。在不依赖人为配置的验证脚本下，自动读取 `test.patch` 提取修改的测试文件，在容器内执行两阶段验证：<br>1️⃣ **Bug复现阶段**：仅打上 `test.patch`，执行测试，验证测试必须**失败**（证明 Bug 真实复现）；<br>2️⃣ **Bug修复阶段**：继续打上 `final.diff`，重新编译并执行测试，验证测试必须**通过**（证明 Bug 成功修复）。<br>目前高度适配 **Python (pytest)**, **Java (maven)**, **C++ (cmake/ctest)**, **Go (go test)**, **JavaScript (mocha/jest)** 五大主流语言。 | **✔️ 是** |
| **M9** | **轨迹字段完备性对比** | 深度递归扫描 `trajectory.json` 与标准样例 `example/trajectory.json` 的所有嵌套字段路径差异（若 Agent 为 `claude code`，会自动剔除部分不适用字段）。 | ❌ |
| **M10** | **系统提示词相似度校验** | 计算 Agent 元数据中 `coding_agent_system_prompt` 与标准模板的相似度，校验比例需 **> 95% 且 != 100%**（既包含标准前置指令，又有 Agent 个性化演进）。若 Agent 为 `claude code` 则自动跳过。 | ❌ |
| **M11** | **自定义一致性校验** | 静态及动态多重验证：<br>1️⃣ 校验 `run_verification.py` 内部是否彻底将 `code.patch` 替换为交付的 `final.diff`，防止残留；<br>2️⃣ 跨文件验证 `instance_id` 的一致性（`instance.json` vs `trajectory.json`）；<br>3️⃣ 对比 `code.patch` 与 `final.diff` 内容重合度；<br>4️⃣ 深度校验 `final.diff` 中所有被修改的文件（经路径清洗），是否**100% 完整被包含**在 `initial_state` 声明的文件名单中，若存在缺失则抛出 `error` 报错。 | ❌ |

---

## 🛠️ 项目环境依赖与安装

1. **Python 环境**：确保安装 Python 3.8 或以上版本。
2. **Docker 服务**：需要安装并运行 Docker 桌面版（Docker Desktop）或 Docker 服务端，确保当前用户有执行 `docker` 命令行工具的权限。
3. **依赖库安装**：
   在终端中运行以下命令安装必要的 Python 依赖包：
   ```bash
   pip install docker loguru
   ```

---

## 🚀 快速上手 (Quick Start)

### 步骤 1：配置质检数据目录
打开根目录下的 `config.json` 文件：
```json
{
    "data_path": "./data",
    "log_path": "./logs"
}
```
*   `data_path`：存放待质检数据集任务的目录。支持**直接存放 `.zip` 格式的压缩包（无需手动解压）**或常规的任务文件夹目录。如果是压缩包，系统在质检运行时会**自动创建临时目录进行安全解包与检验**，并在该任务质检结束时**自动彻底清理临时残留**，确保您的数据目录始终维持整洁。系统同样支持常规文件夹的多层嵌套扫描。
*   `log_path`：质检中产生的控制台日志与质检明细日志输出的根目录。

### 步骤 2：启动批量质检
直接运行主入口程序：
```bash
python main.py
```
**`main.py` 的执行流程为：**
1. 读取 `config.json` 并初始化/迁移本地 SQLite 数据库 `results.db`。
2. 扫描 `data_path` 下的所有任务文件夹作为质检任务。
3. **构建阶段**：自动解析任务 JSON 文件的 `instance_id`，利用当前任务下的 `Dockerfile` 自动构建隔离的 Docker 镜像。
4. **验证阶段**：串行调用 `quality_check.py` 核心质检逻辑，进行 M1-M11 指标验证。
5. 保存本次结果到 SQLite 数据库中。
6. 在终端打印高颜值的 **“全局质检多任务汇总报告”** 仪表盘。

---

## 💻 高级用法 — 单任务命令行驱动

如果您想针对某一个特定的任务目录进行快速的局部质检，可以直接调用核心脚本 `quality_check.py`。

### 命令语法：
```bash
python quality_check.py <任务目录路径> --image <Docker镜像名> --log <日志路径> --report <报告输出路径>
```

### 参数说明：
*   `project_dir` (位置参数)：待质检的任务目录绝对或相对路径。
*   `--image`：选填，若已构建好镜像或拉取好镜像，可通过此参数传入 Docker 镜像名称，以启用 M6、M7、M8 容器级别校验；若不传，则容器类指标会自动跳过（SKIP）。
*   `--log`：指定质检明细日志保存的路径。
*   `--report`：指定质检报告 JSON 文件输出的路径（默认为任务目录下的 `qc_report.json`）。
*   `--quiet`：加入该参数后将开启静默模式，终端不打印输出，只将运行记录留存到日志中。

---

## 💾 数据存取与质检产物

为了便于您对质检结果进行进度跟踪和统计，系统在运行中会自动生成并存储以下质检产物：

1. **SQLite 数据库 (`results.db`)**
   本地将自动建立 SQLite 关系数据库。所有任务的质检最终结果（包括：任务名、是否通过、错误原因、批次批号、运行时间、任务 Prompt）均会录入 `qc_results` 表中。您可以随时使用 SQL 客户端或 Python 脚本读取 `results.db` 提取结果。
2. **终端日志仪表盘 (Console Dashboard)**
   每次批量跑完后，控制台会输出极其直观的可视化报告面板：
   - 📊 全局质检多任务汇总报告，含总任务数、通过数、失败数。
   - 任务目录名称和最终通过状态（`PASS` 为绿，`FAIL` 为红）以及详细错误原因。
   - **模块指标状态面板**：为每个任务文件夹以 `[M1:✓] [M2:✓] [M3:✓] [M4:-]` 的卡片形式绘制 11 个模块的具体状态（`✓` 代表通过，`✗` 代表未通过，`-` 代表跳过/关闭）。
3. **质检明细日志 (`logs/` 目录)**
   为每一个任务在日志输出目录下建立专有文件夹，保存两个核心日志文件：
   - `[任务名].log`：整合了终端完整标准输出（stdout/stderr），便于定位 Docker 构建或回归测试崩溃的原因。
   - `[任务名]_qc.log`：质检系统专属明细日志，记录每一条 Issue 触发的背景与详细参数比对结果。

---

## 🧹 镜像清理辅助工具

Docker 镜像构建频繁会占用大量磁盘空间。系统提供了 `delete_images.py` 辅助脚本，可用于批量删除在质检过程中产生的多余 Docker 镜像。

您可以打开 `delete_images.py`，将 `images` 列表替换为您要清理的镜像标签或 ID，然后运行即可安全卸载镜像：
```bash
python delete_images.py
```
> [!TIP]
> 默认情况下，`main.py` 中的 `DELETE_IMAGE` 变量可控制任务验证通过后是否自动清理镜像。若需腾出空间，可在 `main.py` 中将 `DELETE_IMAGE = True` 取消注释。

---

## ❓ 常见问题排查 (FAQ)

> [!IMPORTANT]
> **Q: 为什么运行 main.py 时直接报错提示 `无法连接到 Docker 服务`？**
> **A**: 请检查您的 Docker 宿主机服务是否开启，且运行该脚本的用户是否具有 `docker` 组的执行权限。您可以通过在终端执行 `docker ps` 来检查 Docker 的连通性。

> [!WARNING]
> **Q: 为什么 M8 (不依赖脚本回归验证) 报告提示 `bug复现失败` 导致质检不通过？**
> **A**: M8 的验证逻辑非常严格，系统会先在打上 `test.patch`（仅测试用例变动）时执行测试。如果测试此时返回值仍为 0（代表没有发生任何报错/断言失败），则说明该测试用例无法复现原 Bug（可能测试用例编写错误、缺少断言、或者测试与环境不匹配）。若无法复现 Bug，则质检直接判定不通过。

> [!NOTE]
> **Q: 如果我想临时跳过 M7 或 M8 回归验证，该如何操作？**
> **A**: 打开 `quality_check.py`，在顶部第 65-77 行左右找到对应的开关：
> - 将 `ENABLE_M7_VERIFICATION` 设为 `False`
> - 将 `ENABLE_M8_NO_DATA_VERIFICATION` 设为 `False`
> 保存后重新运行即可，被关闭的模块在状态面板中会自动显示为 `[-]` 灰色跳过状态。
