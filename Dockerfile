FROM dclong/python-nodejs

# 2. 设置工作目录为 /app (硬性要求)
WORKDIR /app

# 3. 安装系统依赖 (Git 是必须的，Flask 可能需要一些基础库)



# 4. 复制仓库内容


# 5. 安装 Python 依赖
# 注意：如果仓库里有 requirements.txt，直接安装；如果没有，需手动安装常用库
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY font/package.json /app/font/package.json
RUN cd /app/font && npm install
COPY ./ /app
RUN cd /app/font && npm run build
EXPOSE 10001
# 7. 默认启动命令
CMD ["base", "run.sh"]