# Lin Brain Consolidation Plan

**Date**: 2026-02-28  
**Purpose**: Consolidate all Lin data into unified brain before Mac migration and role separation

---

## Current State Analysis

### Data Inventory
- **Total Size**: 459MB
- **Markdown Files**: 54 files
- **Main Directories**:
  - `polymarket-agents/` - Trading bot code & data
  - `projects/` - Project documentation
  - `memory/` - Historical memory files
  - `skills/` - OpenClaw skills
  - `Lin_Brain/` - Previous brain structure

### Core Files
1. **Identity & Persona**
   - `IDENTITY.md` - Role definition
   - `SOUL.md` - Personality & behavior
   - `USER.md` - User profile & preferences
   
2. **Memory & Knowledge**
   - `MEMORY.md` - Permanent memory (critical configs)
   - `memory/` - Daily memory logs
   - `POLYMARKET_STRATEGY_REVISED.md` - Trading strategy
   - `SECURITY.md` - Security protocols

3. **Projects**
   - `projects/auto-trading-bot.md` - Trading bot design
   - `projects/polymarket-arbitrage.md` - Arbitrage strategy
   - `projects/trading-research.md` - Research notes

4. **Technical**
   - `polymarket-agents/` - Full codebase (Python)
   - API integration docs
   - Migration guides

---

## Consolidation Strategy

### Phase 1: Create Unified Brain Archive

**Goal**: Single, comprehensive knowledge base that contains everything Lin needs to know

**Structure**:
```
LIN_UNIFIED_BRAIN/
├── 01_IDENTITY/
│   ├── identity.md
│   ├── soul.md
│   ├── user.md
│   └── capabilities.md
├── 02_MEMORY/
│   ├── permanent_memory.md (MEMORY.md consolidated)
│   ├── project_history.md
│   └── daily_logs/ (all memory/*.md)
├── 03_KNOWLEDGE/
│   ├── trading/
│   │   ├── polymarket_strategy.md
│   │   ├── arbitrage_theory.md
│   │   └── risk_management.md
│   ├── technical/
│   │   ├── polymarket_api.md
│   │   └── openclaw_integration.md
│   └── philosophy/
│       └── quant_research_philosophy.md (from MEMORY.md)
├── 04_PROJECTS/
│   ├── active/
│   │   └── polymarket_bot/
│   └── completed/
├── 05_CODE/
│   └── polymarket-agents/ (full copy)
└── 06_CONFIG/
    ├── env_template.md
    └── security_protocols.md
```

### Phase 2: Role Separation Design

After consolidation, split into specialized agents:

#### 1. Secretary Lin (秘書リン)
**Focus**: Calendar, communication, task management  
**Access to**:
- Identity & User profile
- Task lists & schedules
- Communication logs
- General knowledge

**NOT access to**:
- Trading secrets
- API keys
- Financial data

#### 2. Trader Lin (トレードリン)
**Focus**: Market analysis, trading execution  
**Access to**:
- Trading knowledge base
- Polymarket code & APIs
- Market data & analysis
- Risk management rules

**NOT access to**:
- User's personal schedule
- Non-trading communications

#### 3. Sales Lin (営業リン)
**Focus**: Business development, client relations  
**Access to**:
- Product knowledge
- Client history
- Sales strategies
- Communication templates

**NOT access to**:
- Internal trading strategies
- Sensitive technical details

---

## Migration Workflow

### Step 1: Pre-Migration (on DigitalOcean)
```bash
# Run consolidation script
bash consolidate_brain.sh

# Creates: LIN_UNIFIED_BRAIN.tar.gz
# Size: ~500MB (includes all data + structure)
```

### Step 2: Transfer to Mac
```bash
# On Mac:
scp root@<DO_IP>:/root/openclaw_data/lin/LIN_UNIFIED_BRAIN.tar.gz ~/Downloads/

# Extract
cd ~/openclaw_data
tar -xzf ~/Downloads/LIN_UNIFIED_BRAIN.tar.gz
```

### Step 3: Role Separation (on Mac)
```bash
# Create three separate OpenClaw instances
openclaw init secretary_lin --workspace ~/openclaw_data/secretary_lin
openclaw init trader_lin --workspace ~/openclaw_data/trader_lin
openclaw init sales_lin --workspace ~/openclaw_data/sales_lin

# Populate each with relevant subset of unified brain
```

### Step 4: Access Control Setup
- **Secretary Lin**: READ access to unified brain, WRITE to tasks/schedule
- **Trader Lin**: FULL access to trading data, RESTRICTED access to unified brain
- **Sales Lin**: READ access to business data, NO access to trading secrets

---

## Data Segmentation Rules

### Shared Across All Roles
- User profile (basic)
- Communication style
- Core identity

### Trader Lin ONLY
- API keys (Polymarket, exchange)
- Trading strategies
- Position history
- Risk parameters

### Secretary Lin ONLY
- Calendar
- Personal communications
- Task lists
- Non-sensitive scheduling

### Sales Lin ONLY
- Client database
- Sales pipeline
- Product info
- Marketing materials

---

## Security Considerations

### Critical: Prevent Data Leakage
- Each role has isolated `.env` files
- No cross-role API key sharing
- Separate OpenClaw sessions
- Clear permission boundaries

### Audit Trail
- All role actions logged separately
- Cross-role communication logged
- API usage monitored per role

---

## Next Steps

1. **Confirm design** with user
2. **Create consolidation script**
3. **Run consolidation on DigitalOcean**
4. **Transfer to Mac**
5. **Set up three role-separated instances**
6. **Test each role independently**
7. **Verify no unauthorized cross-access**

---

## Status

- [x] Current state analyzed (459MB, 54 files)
- [x] Consolidation strategy designed
- [x] Role separation architecture defined
- [ ] User approval
- [ ] Implementation scripts created
- [ ] Consolidation executed
- [ ] Mac transfer completed
- [ ] Role instances configured

**Awaiting**: User confirmation to proceed

---

**Last Updated**: 2026-02-28 03:34 JST
