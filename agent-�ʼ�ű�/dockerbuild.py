import os
import json
import re
import docker
import sys
import concurrent.futures
from pathlib import Path


IMAGE_NAME_TEMPLATE = "{pr_id}"



fail_return = {"total": 0, "success": 0, "skipped": 0, "failed": 1}
skipped_return = {"total": 0, "success": 0, "skipped": 1, "failed": 0,"image_name":""}
success_return = {"total": 0, "success": 1, "skipped": 0, "failed": 0,"image_name":""}

BUILD_TIMEOUT = 1800  # 镜像构建超时时间 (30 分钟)


class DockerImageBuilder:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
            print("✅ 成功连接到 Docker 服务。")
        except Exception as e:
            print(f"❌ 错误: 无法连接到 Docker 服务。请确保 Docker 正在运行。")
            print(f"   详细信息: {e}")
            
            

    def parse_instance_id(self, instance_id: str) -> dict | None:
        """解析 instance_id，提取仓库所有者、仓库名称和 PR ID"""
        match = re.match(r"^([^_]+)__(.+?)-(\d+)$", instance_id)
        if match:
            return {
                "repo_owner": match.group(1),
                "repo_name": match.group(2),
                "pr_id": match.group(3),
            }
        else:
            print(f"⚠️ 警告: 无法解析 instance_id '{instance_id}'。格式不匹配。")
            return None

    def check_image_exists(self, image_name: str) -> bool:
        """检查 Docker 镜像是否已存在"""
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False

    def build_image(
        self, json_file_path: Path, image_name: str, force_rebuild: bool = False,
        timeout: int = BUILD_TIMEOUT
    ):
        """构建 Docker 镜像 (实时输出日志, 支持超时机制)"""

        # 检查镜像是否已存在
        if not force_rebuild and self.check_image_exists(image_name):
            print(f"   ✅ 镜像已存在，跳过构建")
            return True

        if force_rebuild and self.check_image_exists(image_name):
            print(f"   🔄 强制重新构建镜像...")
        else:
            print(f"   🔨 开始构建镜像...")

        source_dir = json_file_path.parent.absolute()

        # 检查必要文件是否存在
        dockerfile_path = source_dir / "Dockerfile"
        if not dockerfile_path.exists():
            print(f"   ❌ 错误: Dockerfile 不存在于 {source_dir}")
            return False

        print(f"   -> 构建上下文: {source_dir}")
        print(f"   -> Dockerfile: {dockerfile_path}")
        print(f"   -> 镜像名称: {image_name}")
        print(f"   -> 构建超时: {timeout//60} 分钟")
        print("   --- 构建日志 START ---")

        def _run_build():
            """内部构建函数（在独立线程中执行）"""
            try:
                response = self.client.api.build(
                    path=str(source_dir),
                    tag=image_name,
                    rm=True,
                    forcerm=True,
                    decode=True,
                )

                build_success = True
                for chunk in response:
                    if "stream" in chunk:
                        print(chunk["stream"], end="", flush=True)
                    elif "error" in chunk:
                        print(f"\n❌ 构建错误: {chunk['error']}")
                        build_success = False
                    elif "errorDetail" in chunk:
                        print(f"\n❌ 错误详情: {chunk['errorDetail']}")
                        build_success = False
                    elif "status" in chunk:
                        pass

                return build_success

            except docker.errors.APIError as e:
                print(f"   ❌ Docker API 错误: {e}")
                return False
            except Exception as e:
                print(f"   ❌ 构建时发生未知错误: {e}")
                import traceback
                traceback.print_exc()
                return False

        # 在独立线程中执行构建，支持超时
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_build)
            try:
                build_success = future.result(timeout=timeout)
                print("\n   --- 构建日志 END ---")
                if build_success:
                    print(f"   ✅ 镜像构建成功: {image_name}")
                    return True
                else:
                    print(f"   ❌ 镜像构建失败: {image_name}")
                    return False
            except concurrent.futures.TimeoutError:
                print(f"\n   ❌ 镜像构建超时 (超过 {timeout//60} 分钟)")
                print("   --- 构建日志 END (超时) ---")
                return False

    def process_tasks(
        self, tasks_dir: Path, force_rebuild: bool = False, skip_existing: bool = True,
        timeout: int = BUILD_TIMEOUT
    ):
        """处理任务目录中的所有任务"""
        if not tasks_dir.is_dir():
            print(f"❌ 错误: 任务目录 '{tasks_dir}' 不存在。")
            return fail_return

        print(f"\n🔍 开始扫描目录: {tasks_dir}")
        print(f"   强制重建: {'是' if force_rebuild else '否'}")
        print(f"   跳过已存在: {'是' if skip_existing else '否'}")

        processed_images = set()
        success_count = 0
        skip_count = 0
        fail_count = 0

        for json_file in tasks_dir.rglob("*.json"):
            # 跳过非实例 JSON 文件
            if json_file.name in ("result.json", "results.json", "trajectory.json", "qc_report.json"):
                continue

            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # 检查是否包含 instance_id
                instance_id = data.get("instance_id")
                if not instance_id:
                    print(f"   ❌ 错误: JSON 文件 {json_file} 缺少 instance_id 字段。")
                    return fail_return

                parsed_info = self.parse_instance_id(instance_id)
                if not parsed_info:
                    print(f"   ❌ 错误: JSON 文件 {json_file} 中的 instance_id 无效。")
                    return fail_return

                # 将 parsed_info 中的 repo_owner 和 repo_name 转换为小写
                parsed_info_lower = {
                    "repo_owner": parsed_info["repo_owner"].lower(),
                    "repo_name": parsed_info["repo_name"].lower(),
                    "pr_id": parsed_info["pr_id"],
                }
                image_name = IMAGE_NAME_TEMPLATE.format(**parsed_info_lower)
                skipped_return["image_name"] = image_name
                success_return["image_name"] = image_name
                print(f"   -> 镜像名称: {image_name}")
                print(f"   -> skipped_return: {skipped_return}")
                print(f"   -> success_return: {success_return}")
                # 避免重复处理同一个镜像
                if image_name in processed_images:
                    print(f"   ⚠️  镜像 {image_name} 已处理过，跳过...")
                    skip_count += 1
                    continue 
                
                processed_images.add(image_name)
                print(f"\n{'='*60}")
                print(f"镜像: {image_name}")
                print(f"任务: {instance_id}")
                print(f"{'='*60}")

                # 检查镜像是否已存在
                if (
                    skip_existing
                    and not force_rebuild
                    and self.check_image_exists(image_name)
                ):              
                    print(f"   ✅ 镜像已存在，跳过构建")
                    skip_count += 1
                    continue

                # 构建镜像
                if self.build_image(json_file, image_name, force_rebuild, timeout=timeout):
                    success_count += 1
                else:
                    fail_count += 1

            except json.JSONDecodeError:
                print(f"   -> ⚠️ 跳过无效 JSON 文件: {json_file.name}")
                return fail_return
            except Exception as e:
                print(f"🚨 处理文件 '{json_file}' 时发生错误: {e}")
                import traceback

                traceback.print_exc()
                fail_count += 1
                return fail_return

        # 打印统计信息
        print(f"\n{'='*60}")
        print(f"📊 构建统计:")
        print(f"   总计镜像: {len(processed_images)}")
        print(f"   ✅ 成功构建: {success_count}")
        print(f"   ⏭️  跳过: {skip_count}")
        print(f"   ❌ 失败: {fail_count}")
        print(f"{'='*60}")

        return {
            "total": len(processed_images),
            "success": success_count,
            "skipped": skip_count,
            "failed": fail_count,
            "image_name": image_name,
        }


def build(TASKS_DIR, FORCE_REBUILD, SKIP_EXISTING, timeout=BUILD_TIMEOUT):
    """主函数"""
    print("🐳 Docker 镜像构建工具 (实时输出版)")
    print("=" * 60)

    builder = DockerImageBuilder()
    result = builder.process_tasks(TASKS_DIR, FORCE_REBUILD, SKIP_EXISTING, timeout=timeout)

    return result


if __name__ == "__main__":
    # ==================== 配置区域 ====================
    TASKS_DIR = Path(r"C:\Users\user\work\3.11\ac_test\checkstyle__checkstyle-18384")

    # 构建选项
    FORCE_REBUILD = False  # 是否强制重新构建已存在的镜像
    SKIP_EXISTING = True  # 是否跳过已存在的镜像
    res = build(TASKS_DIR, FORCE_REBUILD, SKIP_EXISTING)
    print(res)
