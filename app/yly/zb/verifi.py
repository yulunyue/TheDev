import os
import json
import re
import docker
from pathlib import Path

TASKS_DIR = Path(r"aesara-devs__aesara-1501")
IMAGE_NAME_TEMPLATE = "swebench/sweb.eval.x_86_64.{repo_owner}_1776_{repo_name}-{pr_id}"


class DockerImageManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
            print("✅ 成功连接到 Docker 服务。")
        except Exception as e:
            print(f"❌ 错误: 无法连接到 Docker 服务。请确保 Docker 正在运行。")
            print(f"   详细信息: {e}")
            exit(1)

    def parse_instance_id(self, instance_id: str) -> dict | None:
        match = re.match(r"^([^_]+)__([^_]+)-(\d+)$", instance_id)
        if match:
            return {
                "repo_owner": match.group(1).lower(),
                "repo_name": match.group(2).lower(),
                "pr_id": match.group(3),
            }
        else:
            print(f"⚠️ 警告: 无法解析 instance_id '{instance_id}'。格式不匹配,已跳过。")
            return None

    def validate_task_data(self, data: dict, filename: str) -> bool:
        """
        校验 JSON 数据字段是否符合要求
        """
        # 1. 定义必须存在的字段
        required_fields = [
            "instance_id",
            "patch",
            "repo",
            "base_commit",
            "hints_text",
            "created_at",
            "test_patch",
            "problem_statement",
            "environment_setup_commit",
            "FAIL_TO_PASS",
            "PASS_TO_PASS",
            "language",
            "content_category",
        ]

        # 2. 定义允许为空的字段 (hints_text, PASS_TO_PASS)
        #    注意：FAIL_TO_PASS 不在这里，说明它不能为空
        allowed_empty_fields = {"hints_text", "PASS_TO_PASS"}

        # --- 基础字段存在性与非空校验 ---
        for field in required_fields:
            if field not in data:
                print(f"   ❌ [校验失败] {filename}: 缺少必须字段 '{field}'")
                return False

            value = data[field]

            # 如果不在允许为空的列表中，则进行非空检查
            if field not in allowed_empty_fields:
                if value is None:
                    print(
                        f"   ❌ [校验失败] {filename}: 字段 '{field}' 不能为空 (None)"
                    )
                    return False
                if isinstance(value, (str, list, dict)) and len(value) == 0:
                    print(
                        f"   ❌ [校验失败] {filename}: 字段 '{field}' 不能为空 (长度为0)"
                    )
                    return False

        # --- Language 校验 ---
        # 允许的值 (全部小写)
        valid_languages = {
            "python",
            "java",
            "typescript",
            "javascript",
            "go",
            "rust",
            "c",
            "c++",
        }

        lang_val = data["language"]
        # 统一转为列表处理 (支持 str 或 list)
        langs_to_check = (
            [lang_val]
            if isinstance(lang_val, str)
            else (lang_val if isinstance(lang_val, list) else [])
        )

        # 再次确认是否有值 (虽然前面非空校验过，但防一手 list 中包含空字符串等情况)
        if not langs_to_check:
            print(f"   ❌ [校验失败] {filename}: language 字段格式无效")
            return False

        for l in langs_to_check:
            if not isinstance(l, str):
                print(f"   ❌ [校验失败] {filename}: language 包含非字符串类型")
                return False
            if l.lower() not in valid_languages:
                print(
                    f"   ❌ [校验失败] {filename}: language '{l}' 无效。允许值: {valid_languages}"
                )
                return False

        # --- Content Category 校验 ---
        # 允许的值
        valid_categories = {
            "计算",
            "通用工具",
            "可视化",
            "系统",
            "时间",
            "网络",
            "加密",
        }

        cat_val = data["content_category"]
        # 统一转为列表处理 (支持 str 或 list)
        cats_to_check = (
            [cat_val]
            if isinstance(cat_val, str)
            else (cat_val if isinstance(cat_val, list) else [])
        )

        if not cats_to_check:
            print(f"   ❌ [校验失败] 