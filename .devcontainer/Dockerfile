FROM ubuntu:24.04

# 非対話モードでのパッケージインストール
ENV DEBIAN_FRONTEND=noninteractive

# 基本パッケージのインストール
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    build-essential \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release \
    sudo \
    sql-migrate \
    nodejs \
    npm \
    pip \
    && rm -rf /var/lib/apt/lists/*

# Pythonのシンボリックリンク作成
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Docker CLIのインストール
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# Docker Composeのインストール
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Voltaのインストール（Node.jsバージョン管理）
RUN curl https://get.volta.sh | bash
ENV VOLTA_HOME="/root/.volta"
ENV PATH="$VOLTA_HOME/bin:$PATH"

# Node.js LTSとpnpmのインストール
RUN /root/.volta/bin/volta install node@lts && \
    /root/.volta/bin/volta install pnpm

# 作業ディレクトリの設定
WORKDIR /workspace

# 開発用ユーザーの作成（オプション）
RUN useradd -m -s /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 環境変数の設定
ENV PYTHONPATH="/workspace"
ENV NODE_ENV="development"

# ポート開放
EXPOSE 3000 8000 5601 9200 3306

# uv と uvx のインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# デフォルトコマンド
CMD ["/bin/bash"]
