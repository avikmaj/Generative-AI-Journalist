#!/bin/bash
# ==============================================================================
# AVIK VIP FACTORY — Environment Setup Script
# Item 9: Verilator + UVM + Z3 + GTKWave + Python + GitHub CLI
# Supports: Ubuntu 22.04 LTS / WSL2 (Ubuntu)
# Run: chmod +x setup_env.sh && ./setup_env.sh
# ==============================================================================

set -e  # exit on any error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # no color

log()    { echo -e "${GREEN}[SETUP]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
check()  { command -v "$1" &>/dev/null && echo -e "${GREEN}✓${NC} $1 found" || echo -e "${RED}✗${NC} $1 missing"; }

# ==============================================================================
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       AVIK VIP FACTORY — Environment Setup          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ------------------------------------------------------------------------------
log "Step 1 — System update"
sudo apt-get update -q

# ------------------------------------------------------------------------------
log "Step 2 — Install Verilator"
sudo apt-get install -y verilator
VERILATOR_VER=$(verilator --version 2>/dev/null | head -1)
log "Installed: $VERILATOR_VER"

# Verify minimum version (5.x required for covergroup support)
MAJOR=$(verilator --version | grep -oP '\d+\.\d+' | head -1 | cut -d. -f1)
if [ "$MAJOR" -lt 5 ]; then
    warn "Verilator < 5.x detected. Covergroup support requires 5.x."
    warn "Install from source: https://verilator.org/guide/latest/install.html"
fi

# ------------------------------------------------------------------------------
log "Step 3 — Install GTKWave (waveform viewer)"
sudo apt-get install -y gtkwave
log "GTKWave: $(gtkwave --version 2>/dev/null | head -1)"

# ------------------------------------------------------------------------------
log "Step 4 — Install Z3 (constraint solver for CRV)"
sudo apt-get install -y z3 python3-z3
log "Z3: $(z3 --version 2>/dev/null)"

# ------------------------------------------------------------------------------
log "Step 5 — Install Python 3 + required packages"
sudo apt-get install -y python3 python3-pip python3-venv
pip3 install --quiet pyyaml jinja2 pytest colorama tabulate
log "Python: $(python3 --version)"

# ------------------------------------------------------------------------------
log "Step 6 — Install Git + GitHub CLI"
sudo apt-get install -y git
# GitHub CLI
type -p curl >/dev/null || sudo apt-get install -y curl
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update -q
sudo apt-get install -y gh
log "Git: $(git --version)"

# ------------------------------------------------------------------------------
log "Step 7 — Install Make + build tools"
sudo apt-get install -y make build-essential

# ------------------------------------------------------------------------------
log "Step 8 — Install UVM (Verilator-compatible)"
# Create UVM directory in home
UVM_DIR="$HOME/uvm"
mkdir -p "$UVM_DIR"

# Download UVM 1.2 source (open source IEEE UVM)
if [ ! -d "$UVM_DIR/src" ]; then
    log "Downloading UVM 1.2 source..."
    git clone --quiet https://github.com/accellera-official/uvm-core.git \
        "$UVM_DIR/src" 2>/dev/null || \
    warn "Could not clone UVM — set UVM_HOME manually if you have a local copy"
fi

# Set UVM_HOME
echo "" >> "$HOME/.bashrc"
echo "# AVIK VIP FACTORY environment" >> "$HOME/.bashrc"
echo "export UVM_HOME=$UVM_DIR/src" >> "$HOME/.bashrc"
echo "export VIP_FACTORY_ROOT=$(pwd)" >> "$HOME/.bashrc"
log "UVM_HOME set to $UVM_DIR/src"

# ------------------------------------------------------------------------------
log "Step 9 — Create project directory structure"
mkdir -p results regression_db logs obj_dir coverage_db

# ------------------------------------------------------------------------------
log "Step 10 — Verify all tools"
echo ""
echo "══════════════════════════════════════"
echo "  TOOL VERIFICATION"
echo "══════════════════════════════════════"
check verilator
check gtkwave
check z3
check python3
check git
check make
echo "══════════════════════════════════════"

# ------------------------------------------------------------------------------
log "Step 11 — Run quick Verilator sanity check"
cat > /tmp/vip_sanity.sv << 'SVEOF'
module vip_sanity;
  initial begin
    $display("Verilator sanity: PASS");
    $finish;
  end
endmodule
SVEOF

verilator --binary /tmp/vip_sanity.sv --Mdir /tmp/vip_sanity_obj \
  -o /tmp/vip_sanity_sim 2>/dev/null && \
  /tmp/vip_sanity_sim && \
  log "Verilator compile+sim: PASS" || \
  warn "Verilator sanity check failed — check installation"

rm -rf /tmp/vip_sanity.sv /tmp/vip_sanity_obj /tmp/vip_sanity_sim

# ------------------------------------------------------------------------------
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║              SETUP COMPLETE                         ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Run: source ~/.bashrc                              ║"
echo "║  Then: python3 dv_runner/dv_runner.py env          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "STATUS: SETUP_COMPLETE"
echo "NEXT:   source ~/.bashrc && python3 dv_runner/dv_runner.py env"
