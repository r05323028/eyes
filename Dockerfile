FROM python:3.7

LABEL authors="seanchang@kklab.com"

# install system requires
RUN apt update && \
    apt install -y libmariadb-dev redis-tools python3-dev

# install python system requires
RUN pip install poetry && \ 
    pip cache purge

# argo cli
RUN curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.1.5/argo-linux-amd64.gz && \
    gunzip argo-linux-amd64.gz && \
    chmod +x argo-linux-amd64 && \
    mv ./argo-linux-amd64 /usr/local/bin/argo

# set workdir
WORKDIR /app

# copy project to workdir
COPY . .
RUN poetry install