# Mac mini Migration Guide

**Date**: 2026-02-25  
**From**: DigitalOcean VPS (Singapore)  
**To**: Mac mini (Local)

---

## Pre-Migration Checklist

### On DigitalOcean (Current)
- [x] Polymarket agents code complete
- [x] Environment variables documented
- [ ] Create full backup of workspace
- [ ] Export critical data/logs
- [ ] Document all running services

### On Mac mini (Target)
- [ ] macOS initial setup complete
- [ ] Admin user configured
- [ ] Internet connection verified
- [ ] Remote access enabled (if needed)

---

## Migration Steps

### Phase 1: Mac mini Initial Setup

#### 1.1 System Setup
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install essential tools
brew install git python@3.9 wget curl
```

#### 1.2 OpenClaw Installation
```bash
# Install Node.js (required for OpenClaw)
brew install node

# Install OpenClaw
npm install -g openclaw

# Verify installation
openclaw --version
```

### Phase 2: Repository Sync

#### 2.1 Clone Repository
```bash
# Create workspace directory
mkdir -p ~/openclaw_data
cd ~/openclaw_data

# Clone from DigitalOcean (via git or direct copy)
# Option A: If using git
git clone <repository_url> lin

# Option B: Direct copy from DigitalOcean
rsync -avz root@<DO_IP>:/root/openclaw_data/lin/ ~/openclaw_data/lin/
```

#### 2.2 Verify Files
```bash
cd ~/openclaw_data/lin
ls -la

# Should see:
# - polymarket-agents/
# - projects/
# - MEMORY.md
# - USER.md
# - SOUL.md
# etc.
```

### Phase 3: Environment Setup

#### 3.1 Python Environment
```bash
cd ~/openclaw_data/lin/polymarket-agents

# Install pyenv (Python version manager)
brew install pyenv

# Install Python 3.9
pyenv install 3.9.25
pyenv local 3.9.25

# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3.2 Environment Variables
```bash
# Copy .env file from DigitalOcean
# (Contains private keys, API keys)

# CRITICAL: Ensure .env contains:
# - POLYGON_WALLET_PRIVATE_KEY
# - OPENAI_API_KEY
# - POLYGON_RPC_URL

# Verify (DO NOT print to screen in shared terminal)
cat .env  # Check locally only
```

### Phase 4: Polymarket Access Test

#### 4.1 IP Address Check
```bash
# Check Mac mini's public IP
curl https://ipapi.co/json/

# Verify country is NOT blocked by Polymarket
# Allowed regions: US, most of Europe, some Asian countries
# Check: https://docs.polymarket.com/developers/CLOB/geoblock
```

#### 4.2 Test Polymarket Connection
```bash
cd ~/openclaw_data/lin/polymarket-agents
source .venv/bin/activate

# Test 1: Check balance (no geo-restriction on read API)
python check_balance.py

# Test 2: Fetch markets
python -c "import requests; print(requests.get('https://gamma-api.polymarket.com/markets?limit=1').status_code)"

# Expected: 200 (success)
# If 403: Geo-restriction still active (may need VPN)
```

#### 4.3 Test Order (Small Amount)
```bash
# Only if Phase 4.2 succeeds
python execute_test_order.py

# This will attempt a $1 test order
# If successful: Mac mini migration complete!
```

### Phase 5: OpenClaw Configuration

#### 5.1 OpenClaw Gateway Setup
```bash
# Start OpenClaw gateway
openclaw gateway start

# Check status
openclaw gateway status

# Configure workspace
openclaw config set workspace ~/openclaw_data/lin
```

#### 5.2 Telegram Integration (if needed)
```bash
# If using Telegram for notifications
# Add Telegram bot token to OpenClaw config
openclaw config set telegram.token <YOUR_TOKEN>
```

---

## Verification Checklist

After migration, verify:

- [ ] OpenClaw runs and responds
- [ ] Polymarket agents can be executed
- [ ] No geo-restriction errors
- [ ] Environment variables loaded correctly
- [ ] Python dependencies installed
- [ ] Test order can be placed (with confirmation)

---

## Rollback Plan

If migration fails:

1. DigitalOcean server remains unchanged (backup)
2. Can continue operations from DigitalOcean
3. Investigate Mac mini issues separately
4. Retry migration when resolved

---

## Security Notes

### Critical Files (Handle with Care)
- `.env` (contains private keys)
- `MEMORY.md` (contains sensitive configs)
- Any files with wallet addresses or API keys

### Best Practices
- **NEVER commit .env to git**
- **NEVER share private keys in chat**
- Use `chmod 600 .env` to restrict file permissions
- Consider using macOS Keychain for sensitive data

---

## Support Resources

- OpenClaw docs: https://docs.openclaw.ai
- Polymarket API: https://docs.polymarket.com
- Python 3.9: https://docs.python.org/3.9/

---

## Timeline

- **Feb 26**: Mac mini arrives → Phase 1 & 2
- **Feb 26-27**: Phase 3 & 4 (environment setup & testing)
- **Feb 28**: Phase 5 (OpenClaw integration)
- **Mar 1**: Full operational on Mac mini

---

**Status**: Ready for migration  
**Last Updated**: 2026-02-25 22:40 JST
