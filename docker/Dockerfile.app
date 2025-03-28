FROM python:3.12-slim

WORKDIR /usr/src/app

# Install Rust and build tools (including gcc)
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    build-essential && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Python dependencies
COPY requirements/app.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "tail", "-f", "/dev/null" ]
