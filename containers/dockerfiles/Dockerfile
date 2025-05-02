ARG UV_BASE=${UV_IMAGE_VER:-0.6.3}
ARG PYTHON_BASE=${PYTHON_IMG_VER:-3.11-slim}

FROM ghcr.io/astral-sh/uv:${UV_BASE} AS uv
FROM python:${PYTHON_BASE} AS base

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    build-essential \
    iputils-ping \
    libmemcached-dev \
    zlib1g-dev \
    curl \
    ca-certificates \
    software-properties-common \
    apt-transport-https \
    sudo \
    postgresql \
    python3-psycopg2 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN mkdir -p /project /mygithub/db /mygithub/logs

## Staging
FROM base AS stage

WORKDIR /project

COPY --from=base /mygithub /mygithub

COPY pyproject.toml uv.lock README.md ./

## Copy monorepo domains
COPY applications/ ./applications/
COPY alembic/ ./alembic/
COPY libs/ ./libs/
COPY packages/ ./packages/
COPY scripts/ ./scripts/
COPY src/ ./src/

## Build
FROM stage AS build

COPY --from=stage /project /project
COPY --from=stage /mygithub /mygithub
COPY --from=uv /uv /usr/bin/uv

WORKDIR /project

## Build project in container
RUN uv sync --all-extras \
    && uv build

## DB migrations
FROM build AS alembic_migrate

COPY --from=build /project /project
COPY --from=build /mygithub /mygithub
COPY --from=uv /uv /usr/bin/uv

WORKDIR /project

RUN echo $PWD && ls && sleep 15

# RUN uv pip install alembic
RUN uv sync --all-extras --dev && \
    uv build
CMD ["/bin/bash", "-c", "uv run alembic stamp head && uv run alembic upgrade head"]

## Scheduled task with schedule Python library
FROM build AS scheduler

COPY --from=build /project /project
COPY --from=build /mygithub /mygithub
COPY --from=uv /uv /usr/bin/uv

WORKDIR /project

CMD ["uv", "run", "scripts/schedules/every_15th_minute_get_stars.py"]
