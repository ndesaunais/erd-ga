# syntax=docker/dockerfile:1.4
FROM public.ecr.aws/docker/library/python:3.11-slim as devcontainer

# Versions
ARG FORCE_REBUILD=4
ARG PIPX_VERSION=1.4.3
ARG POETRY_VERSION=1.8.2


ENV PATH=/opt/pipx/bin:/app/.venv/bin:$PATH \
  PIPX_BIN_DIR=/opt/pipx/bin \
  PIPX_HOME=/opt/pipx/home \
  POETRY_VIRTUALENVS_IN_PROJECT=true
RUN python -m pip install --no-cache-dir --upgrade pip "pipx==$PIPX_VERSION" && \
  pipx install "poetry==$POETRY_VERSION"

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY .devcontainer/devcontainer-setup.sh /devcontainer-setup.sh
RUN /devcontainer-setup.sh

WORKDIR /action/workspace

COPY pyproject.toml poetry.lock /action/workspace/
COPY src/erd_ga/ /action/workspace/src/erd_ga

RUN poetry export --format=requirements.txt --without dev > requirements.txt

# from https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions
# - Docker actions must be run by the default Docker user (root)

RUN python3 -m pip install --no-cache-dir -r requirements.txt

ENV URL="${URL}"
ENV OUTPUT="${OUTPUT}"

ENTRYPOINT python /action/workspace/src/erd_ga/erd_dump.py -u ${URL} -o ${OUTPUT}
