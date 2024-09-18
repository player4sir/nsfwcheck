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

# 设置工作目录
WORKDIR /app

# 复制 requirements 文件到容器
COPY requirements.txt .

# 安装 Python 依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 预下载 opennsfw2 模型权重
RUN curl -L -o /root/.opennsfw2/weights/open_nsfw_weights.h5 \
    https://github.com/bhky/opennsfw2/releases/download/v0.1.0/open_nsfw_weights.h5

# 复制代码到容器中
COPY . .

# 暴露 Flask 服务端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 启动 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]
