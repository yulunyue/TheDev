import subprocess


def delete_docker_image(image_name):
    """
    删除指定的 Docker 镜像
    
    Args:
        image_name: Docker 镜像名称或 ID
    """
    try:
        # 执行 docker rmi 命令删除镜像
        result = subprocess.run(
            ['docker', 'rmi', image_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ 成功删除镜像: {image_name}")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 删除镜像失败: {image_name}")
        print(f"错误信息: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ 错误: 未找到 Docker 命令,请确保 Docker 已安装")
        return False

def delete_docker(images):
    
    
    if not images:
        print("错误: 镜像列表为空")
        return
    
    print(f"准备删除 {len(images)} 个镜像...")
    
    success_count = 0
    for image in images:
        if delete_docker_image(image):
            success_count += 1
    
    print(f"\n完成! 成功删除 {success_count}/{len(images)} 个镜像")

if __name__ == "__main__":

    images = ["swebench/sweb.eval.x_86_64.textualize_1776_rich-2133"]
    delete_docker(images)