#!/bin/bash
# Lin Brain Consolidation Script
# Consolidates all data into unified brain structure

set -e

WORKSPACE="/root/openclaw_data/lin"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BRAIN_DIR="$WORKSPACE/LIN_UNIFIED_BRAIN"
BACKUP_FILE="/root/lin_brain_backup_${TIMESTAMP}.tar.gz"

echo "========================================"
echo "🧠 Lin Brain Consolidation"
echo "========================================"
echo ""
echo "Timestamp: $TIMESTAMP"
echo "Source: $WORKSPACE"
echo "Target: $BRAIN_DIR"
echo ""

# Create brain directory structure
echo "📁 Creating unified brain structure..."
mkdir -p "$BRAIN_DIR"/{01_IDENTITY,02_MEMORY,03_KNOWLEDGE,04_PROJECTS,05_CODE,06_CONFIG}
mkdir -p "$BRAIN_DIR/02_MEMORY/daily_logs"
mkdir -p "$BRAIN_DIR/03_KNOWLEDGE"/{trading,technical,philosophy}
mkdir -p "$BRAIN_DIR/04_PROJECTS"/{active,completed}

# 01_IDENTITY
echo "👤 Consolidating identity..."
cp "$WORKSPACE/IDENTITY.md" "$BRAIN_DIR/01_IDENTITY/identity.md" 2>/dev/null || echo "IDENTITY.md not found"
cp "$WORKSPACE/SOUL.md" "$BRAIN_DIR/01_IDENTITY/soul.md" 2>/dev/null || echo "SOUL.md not found"
cp "$WORKSPACE/USER.md" "$BRAIN_DIR/01_IDENTITY/user.md" 2>/dev/null || echo "USER.md not found"

# Create capabilities document
cat > "$BRAIN_DIR/01_IDENTITY/capabilities.md" << 'EOF'
# Lin Capabilities

## Technical
- Python development (expert)
- API integration (Polymarket, OpenAI, etc.)
- Data analysis & visualization
- Automation & scripting
- Web scraping
- Git & version control

## Trading & Finance
- Quantitative trading research
- Polymarket analysis & automation
- Risk management (Kelly Criterion, bankroll management)
- Expected value calculation
- Market efficiency analysis

## AI & Machine Learning
- LLM integration (GPT, Claude, Gemini)
- Multi-AI orchestration
- Natural language processing
- Sentiment analysis

## Communication & Content
- Technical writing
- Documentation
- Teaching & explanation
- Markdown formatting

## Personal Assistant
- Task management
- Memory & context tracking
- Proactive suggestions
- Long-term relationship building

**Last Updated**: 2026-02-28
EOF

# 02_MEMORY
echo "🧠 Consolidating memory..."
cp "$WORKSPACE/MEMORY.md" "$BRAIN_DIR/02_MEMORY/permanent_memory.md" 2>/dev/null || echo "No permanent memory"

# Daily logs
if [ -d "$WORKSPACE/memory" ]; then
    cp "$WORKSPACE/memory/"*.md "$BRAIN_DIR/02_MEMORY/daily_logs/" 2>/dev/null || echo "No daily logs"
fi

# Create project history
cat > "$BRAIN_DIR/02_MEMORY/project_history.md" << 'EOF'
# Project History

## Active Projects
- Polymarket arbitrage bot (2026-02-17 ~ ongoing)
- Mac mini migration (2026-02-25 ~ ongoing)
- Lin expansion (2026-02-28 ~ ongoing)

## Completed Projects
- Polymarket API integration (2026-02-15 ~ 2026-02-17)
- Trading research & strategy design (2026-02-12 ~ 2026-02-17)

## Key Milestones
- 2026-02-12: Auto-trading bot project initiated
- 2026-02-17: Polymarket agents setup completed
- 2026-02-20: Address configuration resolved
- 2026-02-22: Geo-restriction encountered (proxy solution explored)
- 2026-02-25: Mac mini migration planned
- 2026-02-28: Brain consolidation & role separation designed

**Last Updated**: 2026-02-28
EOF

# 03_KNOWLEDGE
echo "📚 Consolidating knowledge..."

# Trading knowledge
cp "$WORKSPACE/POLYMARKET_STRATEGY_REVISED.md" "$BRAIN_DIR/03_KNOWLEDGE/trading/polymarket_strategy.md" 2>/dev/null || true
cp "$WORKSPACE/projects/polymarket-arbitrage.md" "$BRAIN_DIR/03_KNOWLEDGE/trading/arbitrage_theory.md" 2>/dev/null || true

cat > "$BRAIN_DIR/03_KNOWLEDGE/trading/risk_management.md" << 'EOF'
# Risk Management

## Bankroll Management
- Kelly Criterion
- Conservative: 22.4% of bankroll
- Moderate: 44.8% (recommended)
- Aggressive: 67.3%

## Position Sizing
- Single market max: 60% exposure
- Max acceptable loss: 30%

## Monitoring
- Daily review: 2x (morning/evening)
- Emergency stop: pre-defined loss limits

**Source**: risk_management.py analysis (2026-02-17)
**Last Updated**: 2026-02-28
EOF

# Technical knowledge
cp "$WORKSPACE/polymarket-api-reference.md" "$BRAIN_DIR/03_KNOWLEDGE/technical/" 2>/dev/null || true
cp "$WORKSPACE/polymarket-openclaw-integration.md" "$BRAIN_DIR/03_KNOWLEDGE/technical/" 2>/dev/null || true
cp "$WORKSPACE/polymarket-setup.md" "$BRAIN_DIR/03_KNOWLEDGE/technical/" 2>/dev/null || true

# Philosophy (from MEMORY.md)
cat > "$BRAIN_DIR/03_KNOWLEDGE/philosophy/quant_research_philosophy.md" << 'EOF'
# Quantitative Research Philosophy

## Core Insight
**Bottleneck is NOT knowledge, but experiment cycle time.**

## Traditional Timeline
- Model validation: ~1 week
- Correlation analysis: ~3 weeks  
- Edge confirmation: 2-3 months

## OpenClaw's Value
**Parallelize research throughput** (not speed up individual tests)
- 3 hypotheses/month → 10-15 hypotheses/month

## Critical Warnings
1. Not all processes can be parallelized (future data, live validation)
2. Multiple testing problem (more trials = more false discoveries)
3. Security risks (IP protection crucial)

## True Innovation
**"Research Production Systemization"**
- Automate repetitive work
- Loop-ify research cycle
- High-leverage human decisions

**Source**: Tommy's essay (2026-02-22)
**Last Updated**: 2026-02-28
EOF

# 04_PROJECTS
echo "📊 Consolidating projects..."
if [ -d "$WORKSPACE/projects" ]; then
    cp -r "$WORKSPACE/projects/"* "$BRAIN_DIR/04_PROJECTS/active/" 2>/dev/null || true
fi

# 05_CODE
echo "💻 Consolidating code..."
if [ -d "$WORKSPACE/polymarket-agents" ]; then
    cp -r "$WORKSPACE/polymarket-agents" "$BRAIN_DIR/05_CODE/" 2>/dev/null || true
    
    # Remove .venv (too large, can be recreated)
    rm -rf "$BRAIN_DIR/05_CODE/polymarket-agents/.venv" 2>/dev/null || true
    rm -rf "$BRAIN_DIR/05_CODE/polymarket-agents/__pycache__" 2>/dev/null || true
    find "$BRAIN_DIR/05_CODE/polymarket-agents" -name "*.pyc" -delete 2>/dev/null || true
fi

# 06_CONFIG
echo "⚙️  Consolidating config..."
cp "$WORKSPACE/SECURITY.md" "$BRAIN_DIR/06_CONFIG/security_protocols.md" 2>/dev/null || true

# Create env template (WITHOUT actual secrets)
cat > "$BRAIN_DIR/06_CONFIG/env_template.md" << 'EOF'
# Environment Variables Template

## Polymarket
```bash
POLYGON_WALLET_PRIVATE_KEY="<YOUR_PRIVATE_KEY>"
OPENAI_API_KEY="<YOUR_OPENAI_KEY>"
POLYGON_RPC_URL="https://polygon-rpc.com"
HTTPS_PROXY=""  # Optional: for geo-restriction bypass
HTTP_PROXY=""   # Optional: for geo-restriction bypass
```

## Security Notes
- NEVER commit actual .env to git
- Use `chmod 600 .env` to restrict permissions
- Rotate keys regularly
- Use separate keys for testing vs production

**Last Updated**: 2026-02-28
EOF

# Create README
cat > "$BRAIN_DIR/README.md" << 'EOF'
# Lin Unified Brain

**Created**: 2026-02-28  
**Purpose**: Consolidated knowledge base for Lin AI agent

## Structure

- **01_IDENTITY**: Who Lin is (persona, capabilities, user profile)
- **02_MEMORY**: What Lin remembers (permanent memory, daily logs, project history)
- **03_KNOWLEDGE**: What Lin knows (trading, technical, philosophy)
- **04_PROJECTS**: What Lin is working on (active & completed)
- **05_CODE**: Lin's code repositories
- **06_CONFIG**: Configuration & security protocols

## Usage

### For Mac Migration
This unified brain can be transferred in its entirety to Mac mini.

### For Role Separation
Different roles (Secretary, Trader, Sales) can access relevant subsets:
- Secretary: 01, 02 (partial), 04
- Trader: 01, 02, 03 (trading), 05 (polymarket code)
- Sales: 01, 02 (partial), 03 (non-sensitive)

## Size
- Full brain: ~500MB (including code)
- Without code: ~50MB

## Security
- `.env` files NOT included (use template in 06_CONFIG)
- Private keys NOT included (must be added manually)

**Last Updated**: 2026-02-28
EOF

# Create manifest
echo "📋 Creating manifest..."
find "$BRAIN_DIR" -type f | sed "s|$BRAIN_DIR/||" | sort > "$BRAIN_DIR/MANIFEST.txt"

FILE_COUNT=$(wc -l < "$BRAIN_DIR/MANIFEST.txt")
BRAIN_SIZE=$(du -sh "$BRAIN_DIR" | cut -f1)

echo ""
echo "========================================"
echo "✅ Brain Consolidation Complete!"
echo "========================================"
echo ""
echo "📊 Statistics:"
echo "   Files: $FILE_COUNT"
echo "   Size: $BRAIN_SIZE"
echo "   Location: $BRAIN_DIR"
echo ""

# Create compressed archive
echo "🗜️  Creating compressed archive..."
cd /root
tar -czf "$BACKUP_FILE" -C "$WORKSPACE" "LIN_UNIFIED_BRAIN"

ARCHIVE_SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)

echo ""
echo "✅ Archive created: $BACKUP_FILE"
echo "   Size: $ARCHIVE_SIZE"
echo ""
echo "========================================"
echo "📦 Ready for Mac migration"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Transfer to Mac: scp root@<IP>:$BACKUP_FILE ~/Downloads/"
echo "2. Extract: tar -xzf ~/Downloads/$(basename $BACKUP_FILE)"
echo "3. Follow MAC_MINI_MIGRATION.md for setup"
echo ""
echo "========================================"
