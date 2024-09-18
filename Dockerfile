# 使用 Python 3.9 slim 版本作为基础镜像
FROM python:3.9-slim

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgtk2.0-0 \
    curl && \
    rm -rf /var/lib/apt/lists/*

# 更新 pip 版本
RUN pip install --upgrade pip

# 添加非 root 用户
RUN useradd -ms /bin/bash nonroot

# 切换到非 root 用户
USER nonroot

# 设置工作目录
WORKDIR /app

# 创建权重目录并下载模型
RUN mkdir -p /home/nonroot/.opennsfw2/weights && \
    curl -L -o /home/nonroot/.opennsfw2/weights/open_nsfw_weights.h5 \
    https://github.com/bhky/opennsfw2/releases/download/v0.1.0/open_nsfw_weights.h5

# 复制 requirements 文件到容器
COPY requirements.txt .

# 安装 Python 依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码到容器中
COPY . .

# 暴露 Flask 服务端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 启动 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]
