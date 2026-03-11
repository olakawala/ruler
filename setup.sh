#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════
# Ruler — Penpot + MCP Server Setup
# AI-powered design tool for vibe coding
# ═══════════════════════════════════════════════════════════

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

info()  { echo -e "${GREEN}[+]${RESET} $1"; }
warn()  { echo -e "${YELLOW}[!]${RESET} $1"; }
err()   { echo -e "${RED}[x]${RESET} $1"; }
header() { echo -e "\n${BOLD}── $1 ──${RESET}\n"; }
prompt() { echo -e "${CYAN}[?]${RESET} $1"; }

echo -e "${BOLD}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║           Ruler — Setup                                ║"
echo "║  Penpot + MCP Server for AI-powered design            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# ── Check prerequisites ─────────────────────────────────────

header "Checking prerequisites"

if ! command -v docker &>/dev/null; then
    err "Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
fi
info "Docker found: $(docker --version | head -1)"

if ! docker compose version &>/dev/null; then
    err "Docker Compose v2 is not installed."
    exit 1
fi
info "Docker Compose found: $(docker compose version | head -1)"

# ── Check for existing Penpot ───────────────────────────────

header "Detecting Penpot"

PENPOT_RUNNING=false
if docker ps --format '{{.Names}}' | grep -q 'penpot-backend'; then
    info "Penpot backend is running"
    PENPOT_RUNNING=true
fi

if docker ps --format '{{.Names}}' | grep -q 'penpot-postgres'; then
    info "Penpot PostgreSQL is running"
fi

if [ "$PENPOT_RUNNING" = false ]; then
    echo ""
    prompt "Penpot doesn't seem to be running."
    echo ""
    echo "Options:"
    echo "  [Y] Set up full Penpot stack now (recommended)"
    echo "  [n] Skip Penpot setup (use existing Penpot URL)"
    echo ""
    read -rp "Set up Penpot? [Y/n]: " setup_penpot
    setup_penpot="${setup_penpot:-Y}"
    
    if [[ "$setup_penpot" =~ ^[yY]$ || -z "$setup_penpot" ]]; then
        header "Setting up Penpot"
        
        if [ -f docker-compose.yaml ]; then
            warn "docker-compose.yaml already exists"
            read -rp "Overwrite? (y/N): " overwrite_penpot
            if [[ ! "$overwrite_penpot" =~ ^[yY]$ ]]; then
                info "Using existing docker-compose.yaml"
            else
                rm docker-compose.yaml
                info "Downloading Penpot docker-compose..."
                wget -q https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml
            fi
        else
            info "Downloading Penpot docker-compose..."
            wget -q https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml
        fi
        
        info "Starting Penpot stack (this may take a few minutes)..."
        docker compose -p penpot -f docker-compose.yaml up -d
        
        info "Waiting for Penpot to be ready..."
        max_attempts=60
        attempt=0
        while [ $attempt -lt $max_attempts ]; do
            if curl -sf http://localhost:9001/api/health &>/dev/null; then
                info "Penpot is ready at http://localhost:9001"
                break
            fi
            attempt=$((attempt + 1))
            echo -n "."
            sleep 5
        done
        echo ""
        
        if [ $attempt -eq $max_attempts ]; then
            warn "Penpot may still be starting. Check status with:"
            echo "  docker compose -p penpot -f docker-compose.yaml ps"
        fi
        
        # Extract database password from compose file if not set
        if ! grep -q "PENPOT_DB_PASS=" .env 2>/dev/null || [ -z "${PENPOT_DB_PASS:-}" ]; then
            if grep -q "POSTGRES_PASSWORD=" docker-compose.yaml; then
                export PENPOT_DB_PASS=$(grep "POSTGRES_PASSWORD=" docker-compose.yaml | head -1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
                info "Detected database password from Penpot compose"
            fi
        fi
    else
        echo ""
        echo "Skipping Penpot setup. You'll need to provide your Penpot URL."
        echo ""
    fi
fi

# ── Configuration ───────────────────────────────────────────

header "Configuration"

if [ -f .env ]; then
    warn ".env file already exists."
    read -rp "Overwrite? (y/N): " overwrite
    if [[ ! "$overwrite" =~ ^[yY]$ ]]; then
        info "Keeping existing .env"
    else
        rm .env
    fi
fi

if [ ! -f .env ]; then
    if [ -f .env_example ]; then
        cp .env_example .env
        info "Created .env from .env_example"
    else
        cat > .env << 'EOF'
PENPOT_PUBLIC_URL=http://localhost:9001
PENPOT_ACCESS_TOKEN=
PENPOT_EMAIL=
PENPOT_PASSWORD=
PENPOT_DB_PASS=penpot
MCP_PORT=8787
EOF
        info "Created .env with defaults"
    fi

    echo ""
    echo "Please provide the following configuration values."
    echo "Press Enter to accept the default shown in [brackets]."
    echo ""

    # Public URL
    read -rp "Penpot public URL [http://localhost:9001]: " penpot_url
    penpot_url="${penpot_url:-http://localhost:9001}"
    sed -i "s|PENPOT_PUBLIC_URL=.*|PENPOT_PUBLIC_URL=${penpot_url}|" .env
    info "Public URL: ${penpot_url}"

    # Access Token
    echo ""
    echo "An access token is needed to authenticate with Penpot."
    echo "To create one:"
    echo "  1. Open Penpot in your browser"
    echo "  2. Click your avatar (bottom-left) → Access Tokens"
    echo "  3. Click 'Generate new token'"
    echo "  4. Copy the token"
    echo ""
    echo "Note: You need 'enable-access-tokens' in PENPOT_FLAGS."
    echo "Add it to your Penpot .env file and restart if needed."
    echo ""
    read -rp "Access token (or press Enter to skip): " token
    if [ -n "$token" ]; then
        sed -i "s|PENPOT_ACCESS_TOKEN=.*|PENPOT_ACCESS_TOKEN=${token}|" .env
        info "Access token configured"
    else
        warn "No access token. You can add it to .env later."
        echo ""
        echo "Alternatively, provide email/password credentials:"
        read -rp "Penpot email (or Enter to skip): " email
        if [ -n "$email" ]; then
            read -rsp "Penpot password: " password
            echo ""
            sed -i "s|PENPOT_EMAIL=.*|PENPOT_EMAIL=${email}|" .env
            sed -i "s|PENPOT_PASSWORD=.*|PENPOT_PASSWORD=${password}|" .env
            info "Email/password credentials configured"
        fi
    fi

    # Database password
    echo ""
    if [ -n "${PENPOT_DB_PASS:-}" ]; then
        sed -i "s|PENPOT_DB_PASS=.*|PENPOT_DB_PASS=${PENPOT_DB_PASS}|" .env
        info "Database password: ${PENPOT_DB_PASS}"
    else
        echo "The database password is in your Penpot docker-compose.yml"
        echo "or .env file (look for POSTGRES_PASSWORD or PENPOT_DB_PASS)."
        echo ""
        read -rsp "PostgreSQL password [penpot]: " db_pass
        echo ""
        db_pass="${db_pass:-penpot}"
        sed -i "s|PENPOT_DB_PASS=.*|PENPOT_DB_PASS=${db_pass}|" .env
        info "Database password configured"
    fi

    # MCP Port
    read -rp "MCP server port [8787]: " mcp_port
    mcp_port="${mcp_port:-8787}"
    sed -i "s|MCP_PORT=.*|MCP_PORT=${mcp_port}|" .env
    info "MCP port: ${mcp_port}"
fi

# Load .env for later use
set -a
source .env
set +a

# ── Create combined docker-compose ─────────────────────────

header "Setting up Docker Compose"

# Check if we have a penpot compose file
if [ -f docker-compose.yaml ]; then
    # Create override file that merges MCP with Penpot
    cat > docker-compose.override.yaml << 'COMPOSE_EOF'
services:
  penpot-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: penpot-mcp
    restart: unless-stopped
    ports:
      - "127.0.0.1:8787:8787"
      - "127.0.0.1:4402:4402"
    depends_on:
      penpot-postgres:
        condition: service_healthy
      penpot-backend:
        condition: service_started
    networks:
      - penpot_penpot
    environment:
      PENPOT_BASE_URL: "http://penpot-frontend:8080"
      PENPOT_PUBLIC_URL: "${PENPOT_PUBLIC_URL:-http://localhost:9001}"
      PENPOT_ACCESS_TOKEN: "${PENPOT_ACCESS_TOKEN:-}"
      PENPOT_EMAIL: "${PENPOT_EMAIL:-}"
      PENPOT_PASSWORD: "${PENPOT_PASSWORD:-}"
      PENPOT_DB_HOST: "penpot-postgres"
      PENPOT_DB_PORT: "5432"
      PENPOT_DB_NAME: "penpot"
      PENPOT_DB_USER: "penpot"
      PENPOT_DB_PASS: "${PENPOT_DB_PASS:-penpot}"
      MCP_HOST: "0.0.0.0"
      MCP_PORT: "8787"
      MCP_LOG_LEVEL: "info"
      WS_HOST: "0.0.0.0"
      WS_PORT: "4402"
      PLUGIN_WS_URL: "ws://localhost:4402"
COMPOSE_EOF
    info "Created docker-compose.override.yaml"
else
    err "No docker-compose.yaml found. Please set up Penpot first."
    exit 1
fi

# ── Build MCP Server ───────────────────────────────────────

header "Building Ruler MCP Server"

docker compose build penpot-mcp
info "Docker image built successfully"

# ── Start MCP Server ───────────────────────────────────────

header "Starting Ruler MCP Server"

docker compose up -d penpot-mcp
info "Started MCP server"

# ── Health check ───────────────────────────────────────────

header "Health check"

sleep 5

mcp_port=$(grep MCP_PORT .env 2>/dev/null | cut -d= -f2)
mcp_port="${mcp_port:-8787}"

if curl -sf "http://localhost:${mcp_port}/mcp" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"setup","version":"1.0"}}}' \
    > /dev/null 2>&1; then
    info "MCP server is running on port ${mcp_port}"
else
    warn "Server may still be starting. Check logs with: docker logs penpot-mcp"
fi

# ── Done ────────────────────────────────────────────────────

header "Setup complete"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Ruler is ready!"
echo ""
echo "  • Penpot:      http://localhost:9001"
echo "  • MCP Server:  http://localhost:${mcp_port}/mcp"
echo ""
echo "  To connect Claude Code, add this to your .mcp.json:"
echo ""
echo '  {'
echo '    "mcpServers": {'
echo '      "ruler": {'
echo '        "type": "http",'
echo "        \"url\": \"http://localhost:${mcp_port}/mcp\""
echo '      }'
echo '    }'
echo '  }'
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ "Done!"
"
echo ""
info