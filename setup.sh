#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════
# Ruler — Penpot + MCP Server Setup
# AI-powered design tool for vibe coding
# ═══════════════════════════════════════════════════════════

# ── Parse flags ─────────────────────────────────────────────
DEBUG=false
VERBOSE=false
SKIP_PENPOT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            DEBUG=true
            VERBOSE=true
            ;;
        --verbose|-v)
            VERBOSE=true
            ;;
        --skip-penpot)
            SKIP_PENPOT=true
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --debug         Show all debug output including container logs"
            echo "  --verbose, -v   Show curl commands, docker output"
            echo "  --skip-penpot   Skip Penpot setup (use existing Penpot)"
            echo "  --help, -h      Show this help message"
            exit 0
            ;;
    esac
    shift
done

# ── Colors ──────────────────────────────────────────────────

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
MAGENTA="\033[0;35m"
RESET="\033[0m"

# ── Logging functions ────────────────────────────────────────

info()  { echo -e "${GREEN}[+]${RESET} $1"; }
warn()  { echo -e "${YELLOW}[!]${RESET} $1"; }
err()   { echo -e "${RED}[x]${RESET} $1"; }
header() { echo -e "\n${BOLD}── $1 ──${RESET}\n"; }
prompt() { echo -e "${CYAN}[?]${RESET} $1"; }

verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${MAGENTA}[v]${RESET} $1"
    fi
}

debug() {
    if [ "$DEBUG" = true ]; then
        echo -e "${MAGENTA}[D]${RESET} $1"
    fi
}

# ── Banner ──────────────────────────────────────────────────

echo -e "${BOLD}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║           Ruler — Setup                                ║"
echo "║  Penpot + MCP Server for AI-powered design             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

if [ "$DEBUG" = true ]; then
    echo -e "${MAGENTA}[DEBUG MODE ENABLED]${RESET}"
fi
if [ "$VERBOSE" = true ]; then
    echo -e "${MAGENTA}[VERBOSE MODE ENABLED]${RESET}"
fi
echo ""

# ── Helper: Check if Penpot is ready ─────────────────────────

check_penpot_ready() {
    local endpoints=(
        "http://localhost:9001/"
        "http://localhost:9001/health"
    )
    
    for endpoint in "${endpoints[@]}"; do
        debug "Checking endpoint: $endpoint"
        local status
        status=$(curl -sf -w "%{http_code}" -o /dev/null "$endpoint" 2>/dev/null) || status="000"
        debug "  → HTTP $status"
        
        if [ "$status" = "200" ] || [ "$status" = "301" ] || [ "$status" = "302" ]; then
            verbose "Penpot ready at: $endpoint (HTTP $status)"
            return 0
        fi
    done
    return 1
}

# ── Helper: Show container status ───────────────────────────

show_container_status() {
    verbose "Container status:"
    docker compose -p penpot ps 2>/dev/null | tail -n +2 | while read -r line; do
        verbose "  $line"
    done
    
    if [ "$DEBUG" = true ]; then
        debug "Full container list:"
        docker compose -p penpot ps 2>/dev/null | while read -r line; do
            debug "  $line"
        done
    fi
}

# ── Helper: Show container logs ─────────────────────────────

show_container_logs() {
    local service=$1
    debug "=== $service LOGS (last 30 lines) ==="
    docker compose -p penpot logs --tail=30 "$service" 2>&1 | while read -r line; do
        debug "$line"
    done
    debug "======================================"
}

# ── Check prerequisites ─────────────────────────────────────

header "Checking prerequisites"

if ! command -v docker &>/dev/null; then
    err "Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
fi
info "Docker found: $(docker --version | head -1)"
debug "Docker version: $(docker --version)"

if ! docker compose version &>/dev/null; then
    err "Docker Compose v2 is not installed."
    exit 1
fi
info "Docker Compose found: $(docker compose version | head -1)"
debug "Docker Compose version: $(docker compose version)"

# ── Check for existing Penpot ───────────────────────────────

header "Detecting Penpot"

PENPOT_RUNNING=false
PENPOT_ALREADY_SETUP=false

# Check if containers are running
if docker ps --format '{{.Names}}' | grep -q 'penpot-frontend'; then
    info "Penpot containers are running"
    PENPOT_RUNNING=true
    debug "Found penpot-frontend in running containers"
fi

# Check if docker-compose.yaml exists (Penpot was set up before)
if [ -f docker-compose.yaml ]; then
    info "Found existing docker-compose.yaml"
    PENPOT_ALREADY_SETUP=true
    debug "Penpot was previously set up (docker-compose.yaml exists)"
fi

# ── Penpot Setup Decision ───────────────────────────────────

if [ "$SKIP_PENPOT" = true ]; then
    info "Skipping Penpot setup (--skip-penpot flag)"
elif [ "$PENPOT_RUNNING" = true ]; then
    echo ""
    prompt "Penpot is already running. Use existing or reinstall?"
    echo ""
    echo "  [U] Use existing Penpot (recommended)"
    echo "  [R] Reinstall fresh"
    echo "  [S] Skip Penpot setup entirely"
    echo ""
    read -rp "Choice [U/r/s]: " penpot_choice
    penpot_choice="${penpot_choice:-U}"
    
    if [[ "$penpot_choice" =~ ^[uU]$ ]]; then
        info "Using existing Penpot"
    elif [[ "$penpot_choice" =~ ^[rR]$ ]]; then
        info "Reinstalling Penpot..."
        docker compose -p penpot -f docker-compose.yaml down
        rm docker-compose.yaml
        PENPOT_ALREADY_SETUP=false
        PENPOT_RUNNING=false
    else
        info "Skipping Penpot setup"
        PENPOT_RUNNING=false
        PENPOT_ALREADY_SETUP=false
    fi
fi

# If Penpot not running and not already setup, ask to set up
if [ "$PENPOT_RUNNING" = false ] && [ "$PENPOT_ALREADY_SETUP" = false ]; then
    if [ "$SKIP_PENPOT" = true ]; then
        warn "Penpot not found and --skip-penpot is set. MCP may not work."
    else
        echo ""
        prompt "Penpot doesn't seem to be set up."
        echo ""
        echo "Options:"
        echo "  [Y] Set up full Penpot stack now (recommended)"
        echo "  [n] Skip Penpot setup (use existing Penpot URL manually)"
        echo ""
        read -rp "Set up Penpot? [Y/n]: " setup_penpot
        setup_penpot="${setup_penpot:-Y}"
        
        if [[ "$setup_penpot" =~ ^[yY]$ || -z "$setup_penpot" ]]; then
            SETUP_PENPOT=true
        else
            SETUP_PENPOT=false
        fi
    fi
fi

# ── Setup Penpot ───────────────────────────────────────────

if [ "${SETUP_PENPOT:-false}" = true ]; then
    header "Setting up Penpot"
    
    # Remove any conflicting override files
    if [ -f docker-compose.override.yml ]; then
        rm docker-compose.override.yml
        verbose "Removed old docker-compose.override.yml"
    fi
    
    if [ -f docker-compose.yaml ]; then
        warn "docker-compose.yaml already exists"
        read -rp "Re-download Penpot compose? (y/N): " redownload
        if [[ "$redownload" =~ ^[yY]$ ]]; then
            rm docker-compose.yaml
            info "Re-downloading Penpot docker-compose..."
        else
            info "Using existing docker-compose.yaml"
        fi
    fi
    
    if [ ! -f docker-compose.yaml ]; then
        info "Downloading Penpot docker-compose..."
        verbose "URL: https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml"
        
        if [ "$VERBOSE" = true ] || [ "$DEBUG" = true ]; then
            wget https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml
        else
            wget -q https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml
        fi
    fi
    
    info "Starting Penpot stack (this may take a few minutes)..."
    verbose "Running: docker compose -p penpot -f docker-compose.yaml up -d"
    
    docker compose -p penpot -f docker-compose.yaml up -d
    
    info "Waiting for Penpot to be ready..."
    debug "Starting health check loop (max 60 attempts, 5s interval)"
    
    max_attempts=60
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if check_penpot_ready; then
            info "Penpot is ready at http://localhost:9001"
            break
        fi
        
        attempt=$((attempt + 1))
        printf "."
        
        # Show container status every 12 attempts (every 60 seconds)
        if [ $((attempt % 12)) -eq 0 ] && [ $attempt -gt 0 ]; then
            echo ""
            verbose "Attempt $attempt/$max_attempts - checking containers..."
            show_container_status
        fi
        
        sleep 5
    done
    echo ""
    
    if [ $attempt -eq $max_attempts ]; then
        err "Penpot failed to start within timeout."
        
        warn "Container logs:"
        echo ""
        
        if [ "$DEBUG" = true ]; then
            show_container_logs "penpot-backend"
            show_container_logs "penpot-frontend"
            show_container_logs "penpot-postgres"
        else
            echo "  Run with --debug to see container logs"
        fi
        
        echo ""
        warn "Check status manually: docker compose -p penpot -f docker-compose.yaml ps"
    fi
fi

# Extract database password from compose file if not set
if [ -f docker-compose.yaml ]; then
    if grep -q "POSTGRES_PASSWORD=" docker-compose.yaml 2>/dev/null; then
        DETECTED_DB_PASS=$(grep "POSTGRES_PASSWORD=" docker-compose.yaml | head -1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        debug "Detected POSTGRES_PASSWORD from compose: $DETECTED_DB_PASS"
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
    if [ -n "${DETECTED_DB_PASS:-}" ]; then
        sed -i "s|PENPOT_DB_PASS=.*|PENPOT_DB_PASS=${DETECTED_DB_PASS}|" .env
        info "Database password: ${DETECTED_DB_PASS} (detected from Penpot)"
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

# Remove any conflicting override files first
if [ -f docker-compose.override.yml ]; then
    rm docker-compose.override.yml
    verbose "Removed old docker-compose.override.yml"
fi

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

verbose "Running: docker compose build penpot-mcp"

if [ "$VERBOSE" = true ] || [ "$DEBUG" = true ]; then
    docker compose build penpot-mcp
else
    docker compose build penpot-mcp 2>&1 | while read -r line; do
        verbose "$line"
    done
fi
info "Docker image built successfully"

# ── Start MCP Server ───────────────────────────────────────

header "Starting Ruler MCP Server"

verbose "Running: docker compose up -d penpot-mcp"

if [ "$VERBOSE" = true ] || [ "$DEBUG" = true ]; then
    docker compose up -d penpot-mcp
else
    docker compose up -d penpot-mcp 2>&1 | while read -r line; do
        verbose "$line"
    done
fi
info "Started MCP server"

# ── Health check ───────────────────────────────────────────

header "Health check"

sleep 5

mcp_port=$(grep MCP_PORT .env 2>/dev/null | cut -d= -f2)
mcp_port="${mcp_port:-8787}"

debug "Checking MCP server at http://localhost:${mcp_port}/mcp"

if [ "$DEBUG" = true ]; then
    echo "Sending initialize request to MCP server..."
    echo "Request:"
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"setup","version":"1.0"}}}'
    echo ""
    echo "Response:"
    curl -sf "http://localhost:${mcp_port}/mcp" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"setup","version":"1.0"}}}'
    echo ""
else
    if curl -sf "http://localhost:${mcp_port}/mcp" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"setup","version":"1.0"}}}' \
        > /dev/null 2>&1; then
        info "MCP server is running on port ${mcp_port}"
    else
        warn "Server may still be starting. Check logs with: docker logs penpot-mcp"
        debug "Run: curl -v http://localhost:${mcp_port}/mcp"
    fi
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
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
info "Done!"
