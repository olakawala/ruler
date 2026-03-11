FROM python:3.13-slim AS base

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy pyproject.toml first for dependency resolution
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-dev

# Copy source code - penpot_mcp package
COPY src/ ./src/

# Install the package in editable mode so penpot_mcp module is discoverable
RUN uv pip install -e . --no-deps

# Expose MCP port
EXPOSE 8787
EXPOSE 4402

# Run the MCP server
CMD ["uv", "run", "penpot-mcp"]
