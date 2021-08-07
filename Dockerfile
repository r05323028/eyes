FROM python:3.7

LABEL authors="seanchang@kklab.com"

# install system requires
RUN apt update && \
    apt install -y libmariadb-dev redis-tools python3-dev

# install python system requires
RUN pip install poetry && \ 
    pip cache purge

# set workdir
WORKDIR /app

# copy project to workdir
COPY . .
RUN poetry install