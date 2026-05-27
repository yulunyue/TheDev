
# 基础镜像：Ubuntu 22.04
FROM ubuntu:22.04

LABEL org.opencontainers.image.ref.name=ubuntu
LABEL org.opencontainers.image.version=22.04
# 避免APT等工具在构建过程中请求交互式输入
ENV DEBIAN_FRONTEND=noninteractive

# 1. 基础环境配置：安装必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- 通用工具 ---
    wget \
    git \
    ca-certificates \
    curl \
    vim \
    dos2unix \
    # --- Python 基础 ---
    python3 \
    python3-pip \
    python-is-python3 \
    python3-dev python3-venv autoconf libssl-dev \
    libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev \
    zlib1g-dev pkg-config libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev ffmpeg libgammu-dev build-essential
    

# 2. 安装Miniconda3（Python 3.11）
RUN wget 'https://repo.anaconda.com/miniconda/Miniconda3-py311_23.11.0-2-Linux-x86_64.sh' -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/miniconda3 && \
    rm -f miniconda.sh

# 将Miniconda的可执行文件目录添加到系统PATH
ENV PATH=/opt/miniconda3/bin:${PATH}

# 初始化Conda，使其能够在shell脚本中被调用，并配置conda-forge渠道
RUN conda init bash && \
    conda config --add channels conda-forge && \
    conda config --remove channels defaults

# 3. 复制并执行环境配置脚本 (setup_env.sh)
# 这个脚本负责创建 Conda 虚拟环境和安装基础工具
COPY setup_env.sh /root/setup_env.sh
RUN chmod +x /root/setup_env.sh && \
    # 在一个已初始化Conda的bash环境中执行脚本
    /bin/bash -c "source /root/.bashrc && /root/setup_env.sh"

# 4. 设置工作目录，并配置bash启动时自动激活conda环境
WORKDIR /testbed
# 修改.bashrc文件，这样当启动交互式bash时，会自动激活'testbed'环境
RUN echo "conda activate testbed" >> /root/.bashrc

# 5. 复制并执行仓库配置脚本 (setup_repo.sh)
# 这个脚本负责克隆代码、切换版本和安装项目依赖
COPY setup_repo.sh /root/setup_repo.sh
RUN chmod +x /root/setup_repo.sh && \
    /bin/bash /root/setup_repo.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# 6. 设置最终的默认命令
# 当容器启动时，会进入一个交互式的bash shell，并且会自动激活 'testbed' 环境
CMD ["/bin/bash"]
