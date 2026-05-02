# 1. 基础镜像：选择轻量级 Python 镜像
FROM python:3.10-slim

# 2. 设置工作目录为 /app (硬性要求)
WORKDIR /app

# 3. 安装系统依赖 (Git 是必须的，Flask 可能需要一些基础库)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. 复制仓库内容
COPY repo /app

# 5. 安装 Python 依赖
# 注意：如果仓库里有 requirements.txt，直接安装；如果没有，需手动安装常用库
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt


EXPOSE 5000

# 7. 默认启动命令
CMD ["python", "main.py", "dev"]