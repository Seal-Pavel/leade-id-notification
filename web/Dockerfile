FROM python:3.9-slim as builder

WORKDIR /home/seal

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /home/seal/wheels -r requirements.txt



FROM python:3.9-slim

WORKDIR /home/seal

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    sed -i '/^#.* ru_RU.UTF-8 /s/^#//' /etc/locale.gen && \
    locale-gen ru_RU.utf8

COPY --from=builder /home/seal/wheels /wheels
COPY --from=builder /home/seal/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG assembling_mod
ENV ASSEMBLING_MOD=$assembling_mod

COPY . .