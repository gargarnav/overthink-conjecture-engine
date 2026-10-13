# SPDX-License-Identifier: MIT
# Reproducible environment for the Overthink Conjecture Engine.
#   docker build -t overthink .
#   docker run --rm overthink make test
#   docker run --rm overthink make reproduce-demo
# Lean (adds ~7 GB for the Mathlib cache):
#   docker build -t overthink-lean --build-arg WITH_LEAN=1 .
FROM rust:1.98.1-slim-bookworm

ARG WITH_LEAN=0
ENV PATH="/root/.elan/bin:${PATH}" \
    UV_LINK_MODE=copy

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl git make \
 && rm -rf /var/lib/apt/lists/*

# uv (pinned) manages Python 3.12 from .python-version and installs from the committed lockfile
COPY --from=ghcr.io/astral-sh/uv:0.10.3 /uv /uvx /usr/local/bin/

WORKDIR /app
COPY . .
RUN uv sync --frozen \
 && uv run overthink info
# the project's Python on PATH and libpython on the linker path (PyO3 Rust unit tests)
ENV PATH="/app/.venv/bin:${PATH}"
RUN echo "$(python -c 'import sysconfig; print(sysconfig.get_config_var("LIBDIR"))')" \
      > /etc/ld.so.conf.d/uv-python.conf \
 && ldconfig

# Lean toolchain pinned by lean/lean-toolchain; Mathlib pinned by lean/lake-manifest.json
RUN if [ "$WITH_LEAN" = "1" ]; then \
      curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
        | sh -s -- -y --default-toolchain none \
      && cd lean && lake exe cache get && lake build; \
    fi

CMD ["uv", "run", "overthink", "--help"]
