FROM rust:1.87

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    build-essential \
    pkg-config \
    cmake \
    clang \
    libclang-dev \
    perl \
    ca-certificates \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN rustup toolchain install nightly

WORKDIR /app

COPY . /app

ENTRYPOINT ["bash", "docker/entrypoint.sh"]
