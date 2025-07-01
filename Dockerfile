FROM python:3.12 AS builder

# Atualize os repositórios de pacotes e instale as dependências
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    tdsodbc \
    freetds-bin \
    freetds-common \
    freetds-dev \
    tesseract-ocr \
    gcc \
    libgl1-mesa-glx \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar o FreeTDS e o ODBC
RUN echo "[FreeTDS]\n\
Description = ODBC for FreeTDS\n\
Driver      = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
FileUsage   = 1" > /etc/odbcinst.ini

# Crie o diretório de trabalho no contexto de construção
WORKDIR /build

# Copie o conteúdo necessário para o contexto de construção
COPY . .

# Instale as dependências Python
RUN pip install --no-cache-dir -r /build/requirements.txt

ENV LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/odbc/"