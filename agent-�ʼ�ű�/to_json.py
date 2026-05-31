import json
import os
import re
import shlex
import subprocess
from datetime import date
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# Template Engine (replicates TypeScript TemplateEngine)
# ============================================================================

class TemplateEngine:
    """Resolves {{PLACEHOLDER}} syntax in template strings."""

    def resolve(self, template: str, placeholders: dict[str, Any]) -> str:
        """Replace all {{KEY}} occurrences with placeholder values."""

        def replacer(match: re.Match) -> str:
            key = match.group(1).strip()
            value = placeholders.get(key)
            if value is None:
                return match.group(0)  # Keep unresolved placeholders
            return str(value) if isinstance(value, (str, int, float, bool)) else json.dumps(value)

        return re.sub(r"\{\{([^}]+)\}\}", replacer, template)


# ============================================================================
# Post-processing (replicates PromptBuilder.postProcess)
# ============================================================================

def post_process(prompt: str) -> str:
    """Apply the same post-processing as the TypeScript PromptBuilder."""
    if not prompt:
        return ""

    # Remove multiple consecutive empty lines
    prompt = re.sub(r"\n\s*\n\s*\n", "\n\n", prompt)
    # Trim
    prompt = prompt.strip()
    # Remove trailing ====
    prompt = re.sub(r"====+\s*$", "", prompt)
    # Remove empty sections between separators
    prompt = re.sub(r"\n====+\s*\n+\s*====+\n", "\n====\n", prompt)
    # Remove consecutive empty sections
    prompt = re.sub(r"====\s*\n\s*====\s*\n", "====\n", prompt)
    # Remove empty section headers (## with no content)
    prompt = re.sub(r"^##\s*$[\r\n]*", "", prompt, flags=re.MULTILINE)
    prompt = re.sub(r"\n##\s*$[\r\n]*", "", prompt, flags=re.MULTILINE)
    # Ensure proper section separation
    prompt = re.sub(r"====+\n(?!\n)([^\n])", r"====\n\n\1", prompt)
    prompt = re.sub(r"([^\n])\n(?!\n)====+", r"\1\n\n====", prompt)
    # Clean up any multiple empty lines created
    prompt = re.sub(r"\n\s*\n\s*\n", "\n\n", prompt)
    prompt = prompt.strip()

    return prompt


# ============================================================================
# System Prompt Template Components (from extract_system_prompt.py)
# ============================================================================

AGENT_ROLE = (
    "You are Cline,"
    " a highly skilled software engineer"
    " with extensive knowledge in many programming languages, frameworks, design patterns, and best practices."
)


def tool_use_native(enable_parallel: bool) -> str:
    if enable_parallel:
        return (
            "TOOL USE\n\n"
            "You have access to a set of tools that are executed upon the user's approval."
            " You may use multiple tools in a single response when the operations are independent"
            " (e.g., reading several files, searching in parallel)."
            " For dependent operations where one result informs the next, use tools sequentially."
            " You will receive the results of all tool uses in the user's response."
        )
    else:
        return (
            "TOOL USE\n\n"
            "You have access to a set of tools that are executed upon the user's approval."
            " You may use multiple tools in a single response when the operations are independent"
            " (e.g., reading several files, searching in parallel)."
            " For dependent operations where one result informs the next, use tools sequentially."
            " You will receive the results of all tool uses in the user's response."
        )


TASK_PROGRESS_NATIVE = """UPDATING TASK PROGRESS

You can track and communicate your progress on the overall task using the task_progress parameter supported by every tool call. Using task_progress ensures you remain on task, and stay focused on completing the user's objective. This parameter can be used in any mode, and with any tool call.

- When switching from PLAN MODE to ACT MODE, you must create a comprehensive todo list for the task using the task_progress parameter
- Todo list updates should be done silently using the task_progress parameter - do not announce these updates to the user
- Keep items focused on meaningful progress milestones rather than minor technical details. The checklist should not be so granular that minor implementation details clutter the progress tracking.
- For simple tasks, short checklists with even a single item are acceptable. For complex tasks, avoid making the checklist too long or verbose.
- If you are creating this checklist for the first time, and the tool use completes the first step in the checklist, make sure to mark it as completed in your task_progress parameter.
- Provide the whole checklist of steps you intend to complete in the task, and keep the checkboxes updated as you make progress. It's okay to rewrite this checklist as needed if it becomes invalid due to scope changes or new information.
- If a checklist is being used, be sure to update it any time a step has been completed.
- The system will automatically include todo list context in your prompts when appropriate - these reminders are important.

**How to use task_progress:**
- include the task_progress parameter in your tool calls to provide an updated checklist
- Use standard Markdown checklist format: "- [ ]" for incomplete items and "- [x]" for completed items
- The task_progress parameter MUST be included as a separate parameter in the tool, it should not be included inside other content or argument blocks."""


ACT_VS_PLAN_NATIVE = """ACT MODE V.S. PLAN MODE

In each user message, the environment_details will specify the current mode. There are two modes:

- ACT MODE: In this mode, you have access to all tools EXCEPT the plan_mode_respond tool.
 - In ACT MODE, you use tools to accomplish the user's task. Once you've completed the user's task, you use the attempt_completion tool to present the result of the task to the user.
- PLAN MODE: In this special mode, you have access to the plan_mode_respond tool.
 - In PLAN MODE, the goal is to gather information and get context to create a detailed plan for accomplishing the task, which the user will review and approve before they switch you to ACT MODE to implement the solution.
 - In PLAN MODE, when you need to converse with the user or present a plan, you should use the plan_mode_respond tool to deliver your response directly.

## What is PLAN MODE?

- While you are usually in ACT MODE, the user may switch to PLAN MODE in order to have a back and forth with you to plan how to best accomplish the task. 
- When starting in PLAN MODE, depending on the user's request, you may need to do some information gathering e.g. using read_file or search_files to get more context about the task. You may also ask the user clarifying questions with ask_followup_question to get a better understanding of the task.
- Once you've gained more context about the user's request, you should architect a detailed plan for how you will accomplish the task. Present the plan to the user using the plan_mode_respond tool.
- Then you might ask the user if they are pleased with this plan, or if they would like to make any changes. Think of this as a brainstorming session where you can discuss the task and plan the best way to accomplish it.
- Finally once it seems like you've reached a good plan, ask the user to switch you back to ACT MODE to implement the solution."""


def capabilities_native(cwd: str, supports_browser: bool, yolo_mode: bool) -> str:
    te = TemplateEngine()
    browser_support = ", use the browser" if supports_browser else ""
    ask_followup = "" if yolo_mode else ", and ask follow-up questions"

    browser_capabilities = (
        "\n- You can use the browser_action tool to interact with websites "
        "(including html files and locally running development servers) through "
        "a Puppeteer-controlled browser when you feel it is necessary in "
        "accomplishing the user's task. This tool is particularly useful for "
        "web development tasks as it allows you to launch a browser, navigate "
        "to pages, interact with elements through clicks and keyboard input, "
        "and capture the results through screenshots and console logs. This "
        "tool may be useful at key stages of web development tasks-such as "
        "after implementing new features, making substantial changes, when "
        "troubleshooting issues, or to verify the result of your work. You can "
        "analyze the provided screenshots to ensure correct rendering or "
        "identify errors, and review console logs for runtime issues.\n"
        "\t- For example, if asked to add a component to a react website, you "
        "might create the necessary files, use execute_command to run the site "
        "locally, then use browser_action to launch the browser, navigate to "
        "the local server, and verify the component renders & functions "
        "correctly before closing the browser."
    ) if supports_browser else ""

    template = (
        "CAPABILITIES\n\n"
        "- You have access to tools that let you execute CLI commands on the user's computer,"
        " list files, view source code definitions, regex search{{BROWSER_SUPPORT}},"
        " read and edit files{{ASK_FOLLOWUP}}. These tools help you effectively accomplish"
        " a wide range of tasks, such as writing code, making edits or improvements to"
        " existing files, understanding the current state of a project, performing system"
        " operations, and much more.\n"
        "- When the user initially gives you a task, a recursive list of all filepaths in"
        " the current working directory ('{{CWD}}') will be included in environment_details."
        " This provides an overview of the project's file structure, offering key insights"
        " into the project from directory/file names (how developers conceptualize and"
        " organize their code) and file extensions (the language used). This can also guide"
        " decision-making on which files to explore further. If you need to further explore"
        " directories such as outside the current working directory, you can use the"
        " list_files tool. If you pass 'true' for the recursive parameter, it will list"
        " files recursively. Otherwise, it will list files at the top level, which is better"
        " suited for generic directories where you don't necessarily need the nested"
        " structure, like the Desktop.\n"
        "- You can use search_files to perform regex searches across files in a specified"
        " directory, outputting context-rich results that include surrounding lines. This is"
        " particularly useful for understanding code patterns, finding specific"
        " implementations, or identifying areas that need refactoring.\n"
        "- You can use the list_code_definition_names tool to get an overview of source code"
        " definitions for all files at the top level of a specified directory. This can be"
        " particularly useful when you need to understand the broader context and"
        " relationships between certain parts of the code. You may need to call this tool"
        " multiple times to understand various parts of the codebase related to the task.\n"
        "    - For example, when asked to make edits or improvements you might analyze the"
        " file structure in the initial environment_details to get an overview of the"
        " project, then use list_code_definition_names to get further insight using source"
        " code definitions for files located in relevant directories, then read_file to"
        " examine the contents of relevant files, analyze the code and suggest improvements"
        " or make necessary edits, then use the replace_in_file tool to implement changes."
        " If you refactored code that could affect other parts of the codebase, you could"
        " use search_files to ensure you update other files as needed.\n"
        "- You can use the execute_command tool to run commands on the user's computer"
        " whenever you feel it can help accomplish the user's task. When you need to execute"
        " a CLI command, you must provide a clear explanation of what the command does."
        " Prefer to execute complex CLI commands over creating executable scripts, since"
        " they are more flexible and easier to run. Prefer non-interactive commands when"
        " possible: use flags to disable pagers (e.g., '--no-pager'), auto-confirm prompts"
        " (e.g., '-y' when safe), provide input via flags/arguments rather than stdin,"
        " suppress interactive behavior, etc. For commands that may fail, consider"
        " redirecting stderr to stdout (e.g., `command 2>&1`) so you can see error messages"
        " in the output. For long-running commands, the user may keep them running in the"
        " background and you will be kept updated on their status along the way. Each"
        " command you execute is run in a new terminal instance.{{BROWSER_CAPABILITIES}}"
        "{{WEB_TOOLS_CAPABILITIES}}\n"
        "- You have access to MCP servers that may provide additional tools and resources."
        " Each server may provide different capabilities that you can use to accomplish"
        " tasks more effectively."
    )

    return te.resolve(template, {
        "BROWSER_SUPPORT": browser_support,
        "ASK_FOLLOWUP": ask_followup,
        "BROWSER_CAPABILITIES": browser_capabilities,
        "WEB_TOOLS_CAPABILITIES": "",
        "CWD": cwd,
    })


FEEDBACK_NATIVE = """FEEDBACK

When user is providing you with feedback on how you could improve, you can let the user know to report new issue using the '/reportbug' slash command."""


def rules_native(cwd: str, supports_browser: bool, enable_parallel: bool, has_mcp: bool = False) -> str:
    """Native-next-gen RULES section."""

    browser_wait_rules = (
        " Then if you want to test your work, you might use browser_action to launch the site, "
        "wait for the user's response confirming the site was launched along with a screenshot, "
        "then perhaps e.g., click a button to test functionality if needed, wait for the user's "
        "response confirming the button was clicked along with a screenshot of the new state, "
        "before finally closing the browser."
    ) if supports_browser else ""

    parallel_rule = (
        "\n- You may use multiple tools in a single response when the operations are independent"
        " (e.g., reading several files, creating independent files)."
        " For dependent operations where one result informs the next, use tools sequentially and wait for the user's response."
    ) if enable_parallel else ""

    mcp_rule = (
        "\n- MCP operations should be used one at a time, similar to other tool usage."
        " Wait for confirmation of success before proceeding with additional operations."
    ) if has_mcp else ""

    return f"""RULES

- The current working directory is `{cwd}` - this is the directory where all the tools will be executed from.{parallel_rule}{browser_wait_rules}{mcp_rule}"""


SYSTEM_INFO_TEMPLATE = """SYSTEM INFORMATION

Operating System: {{os}}
IDE: {{ide}}
Default Shell: {{shell}}
Home Directory: {{homeDir}}
Current Working Directory: {{workingDir}}"""


def objective_native(yolo_mode: bool) -> str:
    ask_instruction = (
        " and instead, ask the user to provide the missing parameters using the "
        "ask_followup_question tool"
    ) if not yolo_mode else ""

    return f"""OBJECTIVE

You accomplish a given task iteratively, breaking it down into clear steps and working through them methodically.

1. Analyze the user's task and set clear, achievable goals to accomplish it. Prioritize these goals in a logical order.
2. Work through these goals sequentially, utilizing available tools as necessary. You may call multiple independent tools in a single response to work efficiently. Each goal should correspond to a distinct step in your problem-solving process. You will be informed on the work completed and what's remaining as you go.
3. Remember, you have extensive capabilities with access to a wide range of tools that can be used in powerful and clever ways as necessary to accomplish each goal. First, analyze the file structure provided in environment_details to gain context and insights for proceeding effectively. Then, think about which of the provided tools is the most relevant tool to accomplish the user's task. Next, go through each of the required parameters of the relevant tool and determine if the user has directly provided or given enough information to infer a value. When deciding if the parameter can be inferred, carefully consider all the context to see if it supports a specific value. If all of the required parameters are present or can be reasonably inferred, close the thinking tag and proceed with the tool use. BUT, if one of the values for a required parameter is missing, DO NOT invoke the tool (not even with fillers for the missing params){ask_instruction}. DO NOT ask for more information on optional parameters if it is not provided.
4. Once you've completed the user's task, you must use the attempt_completion tool to present the result of the task to the user. You may also provide a CLI command to showcase the result of your task; this can be particularly useful for web development tasks, where you can run e.g. `open index.html` to show the website you've built.
5. If the task is not actionable, you may use the attempt_completion tool to explain to the user why the task cannot be completed, or provide a simple answer if that is what the user is looking for."""


SKILLS_TEMPLATE = """SKILLS

The following skills provide specialized instructions for specific tasks. When a user's request matches a skill description, use the use_skill tool to load and activate the skill.

Available skills:
{{SKILLS_LIST}}

To use a skill:
1. Match the user's request to a skill based on its description
2. Call use_skill with the skill_name parameter set to the exact skill name
3. Follow the instructions returned by the tool"""


USER_INSTRUCTIONS_TEMPLATE = """USER'S CUSTOM INSTRUCTIONS

The following additional instructions are provided by the user, and should be followed to the best of your ability without interfering with the TOOL USE guidelines.

{{CUSTOM_INSTRUCTIONS}}"""


# ============================================================================
# System Prompt Assembler (native-next-gen variant)
# ============================================================================

def _assemble_native_next_gen(
    te: TemplateEngine,
    os_name: str,
    ide: str,
    shell: str,
    home_dir: str,
    cwd: str,
    supports_browser: bool,
    focus_chain_enabled: bool,
    yolo_mode: bool,
    enable_parallel: bool,
    skills_list: Optional[list[str]],
    custom_instructions: Optional[str],
) -> str:
    """Assemble system prompt using NATIVE_NEXT_GEN variant."""

    sections = [
        AGENT_ROLE,
        tool_use_native(enable_parallel),
    ]

    if focus_chain_enabled:
        sections.append("====\n\n" + TASK_PROGRESS_NATIVE)

    sections.append("====\n\n" + ACT_VS_PLAN_NATIVE)
    sections.append("====\n\n" + capabilities_native(cwd, supports_browser, yolo_mode))

    if skills_list:
        sections.append("====\n\n" + te.resolve(SKILLS_TEMPLATE, {
            "SKILLS_LIST": "\n".join(skills_list),
        }))

    if focus_chain_enabled:
        sections.append("====\n\n" + FEEDBACK_NATIVE)

    sections.append("====\n\n" + rules_native(cwd, supports_browser, enable_parallel))

    sections.append("====\n\n" + te.resolve(SYSTEM_INFO_TEMPLATE, {
        "os": os_name,
        "ide": ide,
        "shell": shell,
        "homeDir": home_dir,
        "workingDir": cwd,
    }))

    sections.append("====\n\n" + objective_native(yolo_mode))

    if custom_instructions:
        sections.append("====\n\n" + te.resolve(USER_INSTRUCTIONS_TEMPLATE, {
            "CUSTOM_INSTRUCTIONS": custom_instructions,
        }))

    full_prompt = "\n\n".join(sections)
    return post_process(full_prompt)


def generate_system_prompt(project_dir: Path) -> str:
    """
    Generate the coding agent system prompt with hardcoded environment parameters.
    
    Args:
        project_dir: The project directory (used to derive cwd via get_repo_path).
    
    Returns:
        The full system prompt string.
    """
    te = TemplateEngine()
    cwd = get_repo_path(project_dir)

    return _assemble_native_next_gen(
        te=te,
        os_name="Linux 6.6",
        ide="Visual Studio Code",
        shell="/bin/bash",
        home_dir="/root",
        cwd=cwd,
        supports_browser=False,
        focus_chain_enabled=True,
        yolo_mode=False,
        enable_parallel=True,
        skills_list=None,
        custom_instructions=None,
    )


# ============================================================================
# Hardcoded Tools (from tools.json)
# ============================================================================

HARDCODED_TOOLS = [
    {
        "name": "ask_followup_question",
        "description": "Ask user a question for clarifying or gathering information needed to complete the task. For example, ask the user clarifying questions about a key implementation decision. You should only ask one question.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The single question to ask the user. E.g. \"How can I help you?\""
                },
                "options": {
                    "type": "string",
                    "description": "An array of 2-5 options (e.x: \"[\"Option 1\", \"Option 2\", \"Option 3\"]\") for the user to choose from. Each option should be a string describing a possible answer to the single question. You may not always need to provide options, but it may be helpful in many cases where it can save the user from having to type out a response manually. IMPORTANT: NEVER include an option to toggle to Act mode, as this would be something you need to direct the user to do manually themselves if needed."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["question", "options"]
        }
    },
    {
        "name": "execute_command",
        "description": "Request to execute a CLI command on the system. Use this when you need to perform system operations or run specific commands to accomplish any step in the user's task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The CLI command to execute. This should be valid for the current operating system. Do not use the ~ character or $HOME to refer to the home directory. Always use absolute paths. The command will be executed from the current workspace, you do not need to cd to the workspace."
                },
                "requires_approval": {
                    "type": "boolean",
                    "description": "To indicate whether this command requires explicit user approval or interaction before it should be executed. For system/file altering operations like installing/uninstalling packages, removing/overwriting files, system configuration changes, network operations, or any commands that are considered potentially dangerous must be set to true. False for safe operations like running development servers, building projects, and other non-destructive operations."
                }
            },
            "required": ["command", "requires_approval"]
        }
    },
    {
        "name": "read_file",
        "description": "Request to read the contents of a file at the specified path. Use this when you need to examine the contents of an existing file you do not know the contents of, for example to analyze code, review text files, or extract information from configuration files. Returned text lines are prefixed with line labels (e.g. `1 |`, `2 |`). These labels are metadata, not part of the file content. For large files, output is automatically limited to 1000 lines. Use start_line and end_line to read specific sections. Automatically extracts raw text from PDF and DOCX files. May not be suitable for other types of binary files, as it returns the raw content as a string. Do NOT use this tool to list the contents of a directory. Only use this tool on files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file to read (relative to the current working directory /testbed/lektor) Use @workspace:path syntax (e.g., @frontend:src/index.ts) to specify a workspace."
                },
                "start_line": {
                    "type": "integer",
                    "description": "The 1-based line number to start reading from (inclusive). Defaults to 1."
                },
                "end_line": {
                    "type": "integer",
                    "description": "The 1-based line number to stop reading at (inclusive). Defaults to start_line + 1000. Use with start_line to read specific sections of large files."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_to_file",
        "description": "[IMPORTANT: Always output the absolutePath first] Request to write content to a file at the specified path. If the file exists, it will be overwritten with the provided content. If the file doesn't exist, it will be created. This tool will automatically create any directories needed to write the file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "absolutePath": {
                    "type": "string",
                    "description": "The absolute path to the file to write to."
                },
                "content": {
                    "type": "string",
                    "description": "After providing the path so a file can be created, then use this to provide the content to write to the file."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["absolutePath", "content"]
        }
    },
    {
        "name": "replace_in_file",
        "description": "[IMPORTANT: Always output the absolutePath first] Request to replace sections of content in an existing file using SEARCH/REPLACE blocks that define exact changes to specific parts of the file. This tool should be used when you need to make targeted changes to specific parts of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "absolutePath": {
                    "type": "string",
                    "description": "The absolute path to the file to write to."
                },
                "diff": {
                    "type": "string",
                    "description": "One or more SEARCH/REPLACE blocks following this exact format:\n  ```\n  ------- SEARCH\n  [exact content to find]\n  =======\n  [new content to replace with]\n  +++++++ REPLACE\n  ```\n  Critical rules:\n  1. SEARCH content must match the associated file section to find EXACTLY:\n     * Match character-for-character including whitespace, indentation, line endings\n     * Include all comments, docstrings, etc.\n  2. SEARCH/REPLACE blocks will ONLY replace the first match occurrence.\n     * Including multiple unique SEARCH/REPLACE blocks if you need to make multiple changes.\n     * Include *just* enough lines in each SEARCH section to uniquely match each set of lines that need to change.\n     * When using multiple SEARCH/REPLACE blocks, list them in the order they appear in the file.\n  3. Keep SEARCH/REPLACE blocks concise:\n     * Break large SEARCH/REPLACE blocks into a series of smaller blocks that each change a small portion of the file.\n     * Include just the changing lines, and a few surrounding lines if needed for uniqueness.\n     * Do not include long runs of unchanging lines in SEARCH/REPLACE blocks.\n     * Each line must be complete. Never truncate lines mid-way through as this can cause matching failures.\n  4. Special operations:\n     * To move code: Use two SEARCH/REPLACE blocks (one to delete from original + one to insert at new location)\n     * To delete code: Use empty REPLACE section\n  5. If your source context came from read_file and includes line labels (for example, \"42 | const x = 1\"), do NOT include the \"42 | \" prefix in SEARCH or REPLACE content. Match only the raw file text."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["absolutePath", "diff"]
        }
    },
    {
        "name": "search_files",
        "description": "Request to perform a regex search across files in a specified directory, providing context-rich results. This tool searches for patterns or specific content across multiple files, displaying each match with encapsulating context.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the directory to search in (relative to the current working directory /testbed/lektor) Use @workspace:path syntax (e.g., @frontend:src/index.ts) to specify a workspace.. This directory will be recursively searched."
                },
                "regex": {
                    "type": "string",
                    "description": "The regular expression pattern to search for. Uses Rust regex syntax."
                },
                "file_pattern": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g., '*.ts' for TypeScript files). If not provided, it will search all files (*)."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["path", "regex"]
        }
    },
    {
        "name": "list_files",
        "description": "Request to list files and directories within the specified directory. If recursive is true, it will list all files and directories recursively. If recursive is false or not provided, it will only list the top-level contents. Do not use this tool to confirm the existence of files you may have created, as the user will let you know if the files were created successfully or not.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the directory to list contents for."
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Whether to list files recursively. Use true for recursive listing, false or omit for top-level only."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_code_definition_names",
        "description": "Request to list definition names (classes, functions, methods, etc.) used in source code files at the top level of the specified directory. This tool provides insights into the codebase structure and important constructs, encapsulating high-level concepts and relationships that are crucial for understanding the overall architecture.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of a directory (not a file) relative to the current working directory /testbed/lektor Use @workspace:path syntax (e.g., @frontend:src/index.ts) to specify a workspace.. Lists definitions across all source files in that directory. To inspect a single file, use read_file instead."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "access_mcp_resource",
        "description": "Request to access a resource provided by a connected MCP server. Resources represent data sources that can be used as context, such as files, API responses, or system information. You must only use this tool if you have been informed of the MCP server and the resource you are trying to access.",
        "input_schema": {
            "type": "object",
            "properties": {
                "server_name": {
                    "type": "string",
                    "description": "The name of the MCP server providing the resource"
                },
                "uri": {
                    "type": "string",
                    "description": "The URI identifying the specific resource to access"
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress after this tool use is completed. The task_progress parameter must be included as a separate parameter inside of the parent tool call, it must be separate from other parameters such as content, arguments, etc. (See 'UPDATING TASK PROGRESS' section for more details)"
                }
            },
            "required": ["server_name", "uri"]
        }
    },
    {
        "name": "attempt_completion",
        "description": "Once you've completed the user's task, use this tool to present the final result to the user, including a brief and very short (1-2 paragraph) summary of the task and what was done to resolve it. Provide the basics, hitting the highlights, but do delve into the specifics. You should only call this tool when you have completed all tasks in the task_progress list, and completed all changes that are necessary to satisfy the user's request. You should not provide the contents of the task_progress list in the result parameter, it must be included in the task_progress parameter.",
        "input_schema": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "string",
                    "description": "A clear, brief and very short (1-2 paragraph) summary of the final result of the task."
                },
                "command": {
                    "type": "string",
                    "description": "An actionable terminal command that is non-verbose that allows user to review the result of your work. For example, use `start localhost:3000` to start a locally running development server. Commands like `echo` or `cat` that merely print text or open a file are not allowed. Ensure the command is properly formatted for user's OS and does not contain any harmful instructions"
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress with the latest status of each subtasks included previously, if any. If you are calling attempt completion, and all items in this list have been completed, they must be marked as completed in this response."
                }
            },
            "required": ["result"]
        }
    },
    {
        "name": "plan_mode_respond",
        "description": "Respond to the user's inquiry in an effort to plan a solution to the user's task. This tool should ONLY be used when you have already explored the relevant files and are ready to present a concrete plan. DO NOT use this tool to announce what files you're going to read - just read them first. This tool is only available in PLAN MODE. The environment_details will specify the current mode; if it is not PLAN_MODE then you should not use this tool.\nHowever, if while writing your response you realize you actually need to do more exploration before providing a complete plan, you can add the optional needs_more_exploration parameter to indicate this. This allows you to acknowledge that you should have done more exploration first, and signals that your next message will use exploration tools instead.",
        "input_schema": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "description": "The response to provide to the user."
                },
                "task_progress": {
                    "type": "string",
                    "description": "A checklist showing task progress with the latest status of each subtasks included previously if any."
                }
            },
            "required": ["response"]
        }
    },
    {
        "name": "load_mcp_documentation",
        "description": "Load documentation about creating MCP servers. This tool should be used when the user requests to create or install an MCP server (the user may ask you something along the lines of \"add a tool\" that does some function, in other words to create an MCP server that provides tools and resources that may connect to external APIs for example. You have the ability to create an MCP server and add it to a configuration file that will then expose the tools and resources for you to use with `use_mcp_tool` and `access_mcp_resource`). The documentation provides detailed information about the MCP server creation process, including setup instructions, best practices, and examples.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "generate_explanation",
        "description": "Opens a multi-file diff view and generates AI-powered inline comments explaining the changes between two git references. Use this tool to help users understand code changes from git commits, pull requests, branches, or any git refs. The tool uses git to retrieve file contents and displays a side-by-side diff view with explanatory comments.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "A descriptive title for the diff view (e.g., 'Changes in commit abc123', 'PR #42: Add authentication', 'Changes between main and feature-branch')"
                },
                "from_ref": {
                    "type": "string",
                    "description": "The git reference for the 'before' state. Can be a commit hash, branch name, tag, or relative reference like HEAD~1, HEAD^, origin/main, etc."
                },
                "to_ref": {
                    "type": "string",
                    "description": "The git reference for the 'after' state. Can be a commit hash, branch name, tag, or relative reference. If not provided, compares to the current working directory (including uncommitted changes)."
                }
            },
            "required": ["title", "from_ref"]
        }
    },
    {
        "name": "use_subagents",
        "description": "Run up to five focused in-process subagents in parallel. Each subagent gets its own prompt and returns a comprehensive research result with tool and token stats. Use this for broad exploration when reading many files would consume the main agent's context window. You do not need to launch multiple subagents every time; using one subagent is valid when it avoids unnecessary context usage for light discovery work.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt_1": {
                    "type": "string",
                    "description": "First subagent prompt."
                },
                "prompt_2": {
                    "type": "string",
                    "description": "Optional second subagent prompt."
                },
                "prompt_3": {
                    "type": "string",
                    "description": "Optional third subagent prompt."
                },
                "prompt_4": {
                    "type": "string",
                    "description": "Optional fourth subagent prompt."
                },
                "prompt_5": {
                    "type": "string",
                    "description": "Optional fifth subagent prompt."
                }
            },
            "required": ["prompt_1"]
        }
    }
]


# ============================================================================
# Original to_json.py functions
# ============================================================================

def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_repo_relative_path(path: str) -> str:
    normalized = path.replace("\\", "/").strip()
    if normalized.startswith("a/") or normalized.startswith("b/"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("/")
    parts = normalized.split("/")
    if len(parts) >= 3 and parts[0] == "testbed":
        normalized = "/".join(parts[2:])
    return normalized


def parse_non_added_files(final_diff: str) -> list[str]:
    """解析 final.diff，返回所有非新增（即修改过的）文件列表"""
    required_files: list[str] = []
    current_old_path: str | None = None
    current_is_new_file = False

    for raw_line in final_diff.splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("diff --git a/") and " b/" in line:
            if current_old_path and not current_is_new_file:
                required_files.append(current_old_path)
            current_old_path = normalize_repo_relative_path(
                line[len("diff --git a/") :].split(" b/", 1)[0]
            )
            current_is_new_file = False
            continue

        if current_old_path is None:
            continue

        if line.startswith("new file mode") or line.startswith("--- /dev/null"):
            current_is_new_file = True

    if current_old_path and not current_is_new_file:
        required_files.append(current_old_path)

    return sorted(dict.fromkeys(required_files))


def load_trajectory_record(project_dir: Path) -> dict:
    trajectory_path = project_dir / "trajectory.json"
    if not trajectory_path.is_file():
        return {}

    content = read_text(trajectory_path).strip()
    if not content:
        return {}

    try:
        obj = json.loads(content)
    except json.JSONDecodeError:
        return {}

    if isinstance(obj, dict):
        return obj
    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        return obj[0]
    return {}


def get_repo_path(project_dir: Path) -> str:
    setup_repo_path = project_dir / "setup_repo.sh"
    if setup_repo_path.is_file():
        for raw_line in read_text(setup_repo_path).splitlines():
            line = raw_line.strip()
            if not line.startswith("git clone"):
                continue
            target = line.split()[-1].strip()
            if target.startswith("/testbed/"):
                return target.rstrip("/")
            break

    record = load_trajectory_record(project_dir)
    instance = record.get("instance", {})
    if isinstance(instance, dict):
        repo = instance.get("repo", "")
        if isinstance(repo, str) and repo.strip():
            repo_name = repo.rstrip("/").split("/")[-1]
            if repo_name:
                return f"/testbed/{repo_name}"

    return "/testbed"


def run_command(cmd: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def start_container(image_name: str) -> str:
    result = run_command(["docker", "run", "-d", "--rm", image_name, "sleep", "3600"])
    if result.returncode != 0:
        raise RuntimeError(f"failed to start container: {result.stderr.strip()}")
    return result.stdout.strip()


def stop_container(container_id: str) -> None:
    run_command(["docker", "stop", container_id], timeout=30)


def read_file_from_container(container_id: str, file_path: str) -> str:
    result = run_command(
        ["docker", "exec", container_id, "bash", "-lc", f"cat -- {shlex.quote(file_path)}"],
        timeout=60,
    )
    if result.returncode != 0:
        raise FileNotFoundError(
            f"failed to read {file_path} from container: {result.stderr.strip()}"
        )
    return result.stdout


def export_files_from_image(project_dir: Path, image_name: str) -> dict[str, str]:
    """从 Docker 镜像中导出 final.diff 涉及的非新增文件的原始内容"""
    final_diff = read_text(project_dir / "final.diff")
    if not final_diff.strip():
        raise FileNotFoundError(f"final.diff not found or empty: {project_dir / 'final.diff'}")

    target_files = parse_non_added_files(final_diff)
    repo_path = get_repo_path(project_dir)

    container_id = start_container(image_name)
    try:
        result: dict[str, str] = {}
        for relative_path in target_files:
            container_path = f"{repo_path.rstrip('/')}/{relative_path}"
            result[relative_path] = read_file_from_container(container_id, container_path)
        return result
    finally:
        stop_container(container_id)


def get_image_name_from_dir() -> str:
    """
    从当前目录名中提取镜像名。
    目录命名规范：仓库所有者_仓库名-pr编号
    例如：octocat_hello-world-pr42 -> 镜像名为 42
    """
    dir_name = os.path.basename(os.getcwd())
    match = re.search(r'-pr(\d+)$', dir_name)
    if match:
        return match.group(1)
    # 如果无法从目录名提取，返回空字符串，后续可回退
    return ""


def extract_file_content(text):
    """从文本中提取文件路径和内容"""
    pattern = r'\[read_file for \'([^\']+)\'\]\s*Result:\n(.*)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        filepath = match.group(1).strip()
        content = match.group(2).strip()
        return filepath, content
    return None, None


def get_filename(filepath):
    """从文件路径中提取文件名"""
    return filepath.split('/')[-1] if '/' in filepath else filepath


def normalize_path(filepath):
    filepath = filepath.replace("\\", "/").strip()
    while filepath.startswith("./"):
        filepath = filepath[2:]
    filepath = re.sub(r"^/?testbed/[^/]+/", "", filepath)
    filepath = re.sub(r"^.*?/testbed/[^/]+/", "", filepath)
    return filepath.lstrip("/")


def extract_patch_paths(patch_text):
    paths = set()
    for line in patch_text.splitlines():
        candidates = []
        if line.startswith("diff --git "):
            parts = line.split()
            candidates = parts[2:4]
        elif line.startswith("--- a/") or line.startswith("+++ b/"):
            candidates = [line[4:].strip()]
        for candidate in candidates:
            candidate = normalize_path(candidate)
            if candidate.startswith(("a/", "b/")):
                candidate = candidate[2:]
            if candidate and candidate != "/dev/null":
                paths.add(candidate)
    return paths


def load_known_patch_paths():
    paths = set()
    for patch_file in ("final.diff", "code.patch", "test.patch"):
        if os.path.exists(patch_file):
            with open(patch_file, "r", encoding="utf-8") as f:
                paths.update(extract_patch_paths(f.read()))
    return paths


def normalize_initial_state_path(filepath, known_patch_paths):
    filepath = normalize_path(filepath)
    if filepath in known_patch_paths:
        return filepath
    for known_path in sorted(known_patch_paths, key=len, reverse=True):
        if filepath.endswith("/" + known_path):
            return known_path
    known_roots = {path.split("/", 1)[0] for path in known_patch_paths if "/" in path}
    for root in sorted(known_roots, key=len, reverse=True):
        marker = "/" + root + "/"
        if marker in filepath:
            return filepath[filepath.index(marker) + 1:]
    return filepath


# ============================================================================
# Main conversion function
# ============================================================================

def convert_json_to_json(input_file, output_file, image_name=""):
    # 从输入文件路径中提取task_id（路径中最后一个反斜杠前的数字）
    task_id = ""
    path_parts = input_file.replace("\\", "/").split("/")
    for part in path_parts:
        if re.match(r'^\d+$', part):  # 检查是否为纯数字
            task_id = part
            break
    # 读取输入JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 初始化字典 - 使用从镜像导出的方式构建 INITIAL_STATE
    INITIAL_STATE = {}
    
    # 如果未指定镜像名，尝试从当前目录名自动提取
    if not image_name:
        image_name = get_image_name_from_dir()
    
    # 尝试从 Docker 镜像导出文件作为 initial_state
    if image_name:
        try:
            project_dir = Path.cwd()
            INITIAL_STATE = export_files_from_image(project_dir, image_name)
            print(f"从镜像 {image_name} 导出了 {len(INITIAL_STATE)} 个文件到 initial_state")
        except Exception as e:
            print(f"从镜像导出文件失败: {e}")
            print("将使用空的 initial_state")
    else:
        print("未指定镜像名且无法从目录名自动提取，将使用空的 initial_state")
    
    # 提取轨迹数据
    trajectory = data
    system_prompt = []  # 存储system_prompt
    turn_count = 0  # 计算轮次
    instruction = ""
    modelId = ""
    for item in data:
        if item["role"] == "user":
            user_content_parts = []
            
            # 处理user的content
            for content_item in item["content"]:
                if content_item["type"] == "text":
                    text = content_item["text"].strip()
                    if text:
                        user_content_parts.append({
                            "type": "text",
                            "text": text
                        })
            # 将所有user的content添加到system_prompt
            if user_content_parts:
                for content_part in user_content_parts:
                    system_prompt.append({
                        "type": content_part["type"],
                        "text": content_part["text"]
                    })
        elif item["role"] == "assistant":
            assistant_content = []
            # 处理assistant的content
            for content_item in item["content"]:
                if content_item["type"] == "thinking":
                    # 保持thinking类型，包含thinking字段
                    thinking_content = {
                        "type": "thinking",
                        "thinking": content_item.get("thinking", "")
                    }
                    if "summary" in content_item:
                        thinking_content["summary"] = content_item["summary"]
                    assistant_content.append(thinking_content)
                
                elif content_item["type"] == "tool_use":
                    # 转换为tool_use类型，包含id、name、input字段
                    assistant_content.append({
                        "type": "tool_use",
                        "id": content_item.get("id", ""),
                        "name": content_item.get("name", ""),
                        "input": content_item.get("input", {})
                    })
                
                elif content_item["type"] == "text":
                    # 保持text类型
                    assistant_content.append({
                        "type": "text",
                        "text": content_item.get("text", "")
                    })
            
            # 计算轮次：每遇到一个assistant就增加一轮
            if item["role"] == "assistant":
                turn_count += 1
            
            # 保存最后一个modelInfo.modelId
            if "modelInfo" in item:
                modelId = item["modelInfo"]["modelId"]
    # 将system_prompt的第一个元素的text添加到instruction
    instruction = data[0]["content"][0]["text"]
    
    # 读取final.diff文件
    final_diff = ""
    diff_file = "final.diff"
    if os.path.exists(diff_file):
        with open(diff_file, 'r', encoding='utf-8') as f:
            final_diff = f.read()
    
    # 读取当前目录下的json文件，取其中的instance_id字段作为instance_id，取其中的repo字段作为repo...
    instance_id = ""
    base_commit = ""
    fail_to_pass = []
    pass_to_pass = []
    repo = ""
    language = ""
    problem_statement = ""
    for file in os.listdir("."):
        if file.endswith(".json"):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "instance_id" in data:
                    instance_id = data["instance_id"]
                if "repo" in data:
                    repo = data["repo"]
                if "base_commit" in data:
                    base_commit = data["base_commit"]
                if "FAIL_TO_PASS" in data:
                    fail_to_pass = data["FAIL_TO_PASS"]
                if "PASS_TO_PASS" in data:
                    pass_to_pass = data["PASS_TO_PASS"]
                if "language" in data:
                    language = data["language"]
                if "problem_statement" in data:
                    problem_statement = data["problem_statement"]
    # 从instruction中提取problem_statement
    if not problem_statement:
        if "以下是具体的issue描述：" in instruction:
            print(000)
            problem_statement = instruction.split("以下是具体的issue描述：")[1].strip()
        else:
            problem_statement = instruction.split("以下是issue：")[1].strip()
        if not problem_statement:
            problem_statement = instruction.split("以下是issue描述：")[1].strip()

    # 提取当前文件夹中test.patch文件的内容作为test_patch
    test_patch = ""
    test_file = "test.patch"
    if os.path.exists(test_file):
        with open(test_file, 'r', encoding='utf-8') as f:
            test_patch = f.read()
    # 提取当前文件夹中code.patch文件的内容作为patch
    patch = ""
    patch_file = "code.patch"
    if os.path.exists(patch_file):
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch = f.read()
    thinking_mode = ""
    # 判断trajectory中的"role": "assistant"数据的content数组中是否有type为thinking的元素
    for item in trajectory:
        if item["role"] == "assistant":
            for content_item in item["content"]:
                if content_item["type"] == "thinking":
                    thinking_mode = "slow"
                    break
            else:
                thinking_mode = "fast"
                break
    
    if thinking_mode == "":
        thinking_mode = "fast"

    # 使用 generate_system_prompt 生成 coding_agent_system_prompt
    project_dir = Path.cwd()
    coding_agent_system_prompt = generate_system_prompt(project_dir)
    print(f"已通过 generate_system_prompt 生成 coding_agent_system_prompt（cwd: {get_repo_path(project_dir)}）")

    # 使用硬编码的 tools
    tools = HARDCODED_TOOLS
    print(f"使用硬编码 tools（共 {len(tools)} 个工具）")

    # 构建输出JSON对象
    output_data = {
        "instance_id": instance_id,
        "instruction": instruction,
        "instance": {
            "repo": repo,
            "base_commit": base_commit,
            "git_context": {
                "initial_state": INITIAL_STATE,
                "final_diff": final_diff
            },
            "problem_statement": problem_statement,
            "FAIL_TO_PASS": fail_to_pass,
            "PASS_TO_PASS": pass_to_pass,
            "patch": patch,
            "test_patch": test_patch,
        },
        "metadata": {
            "agent": "cline",
            "model": modelId,
            "thinking_mode": thinking_mode,
            "eval_output_dir": "/testbed",
            "data_source": "GitHub开源仓库",
            "source": "后端工程师",
            "coding_agent_system_prompt": coding_agent_system_prompt,
            "tools": tools
        },
        "trajectory": trajectory,
        "task_category": "",
        "metrics": {
            "turn_count": turn_count
        },
        "language": language
    }
    
    # 写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output_data, ensure_ascii=False, indent=2))
    
    print(f"转换完成！已保存到 {output_file}")
    print(f"提取了 {len(INITIAL_STATE)} 个文件到 initial_state")
    print(f"系统提示词包含 {len(system_prompt)} 个项目")
    print(f"总共有 {turn_count} 轮对话")


if __name__ == "__main__":
    # 输入和输出文件路径
    metadata_dir = "1778755187175"  # 修改为你的输入文件路径
    input_json_file = os.path.join(metadata_dir, "api_conversation_history.json")
    output_json_file = "trajectory.json"  # 输出文件路径
    
    # 镜像名默认为空，脚本会自动从当前目录名提取
    # 如果需要手动指定，可以在这里设置
    image_name = "" 
    
    convert_json_to_json(input_json_file, output_json_file, image_name)
