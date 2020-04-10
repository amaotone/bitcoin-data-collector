FROM python:3.7-slim as builder
WORKDIR /work
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /work
COPY --from=builder /work/requirements.txt .
RUN pip install -r requirements.txt
