FROM python:3.13-slim AS base

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy source code first
COPY src/ ./src/

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-dev

# Set PYTHONPATH so penpot_mcp module can be found
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose MCP port
EXPOSE 8787
EXPOSE 4402

# Run the MCP server
CMD ["uv", "run", "penpot-mcp"]
